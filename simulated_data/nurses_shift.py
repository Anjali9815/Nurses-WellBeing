import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)
N_NURSES = 150
N_SUPERVISORS = 12

# 1. nurses.csv - Demographics and professional identity
nurse_genders = np.random.choice(['Female', 'Male', 'Nonbinary'], N_NURSES, p=[.88,.11,.01])
nurses = pd.DataFrame({
    'nurse_id': [f"N{str(i+1).zfill(4)}" for i in range(N_NURSES)],
    'first_name': np.random.choice(['Alex','Taylor','Jamie','Morgan','Sam','Jordan','Chris','Jess','Drew','Casey'], N_NURSES),
    'last_name': np.random.choice(['Smith','Brown','Lee','Patel','Garcia','Davis','Chen','Nguyen','Wong','Martinez'], N_NURSES),
    'gender': nurse_genders,
    'age': np.random.choice(range(21,65),N_NURSES),
    'race_ethnicity': np.random.choice(['White','Black','Asian','Hispanic','Other','Multiracial'], N_NURSES, p=[0.73, 0.09, 0.09, 0.07, 0.01, 0.01]), 
    'education_nurse': np.random.choice(['Diploma','Associate','Baccalaureate','Masters','Doctorate'], N_NURSES, p=[0.04,0.20,0.60,0.13,0.03]),
    'years_licensed': np.random.choice(range(1,42),N_NURSES),
    'license_type': np.random.choice(['RN','APRN','LPN'],N_NURSES,p=[0.80,0.13,0.07]),
    'primary_setting': np.random.choice(['Hospital','Nursing home','Home health','Clinic','Ambulatory'],N_NURSES, p=[0.60,0.13,0.11,0.09,0.07]),
    'specialty': np.random.choice(['Med-surg','Emergency','Geriatrics','Pediatrics','Psychiatry','Cardiac','Other'],N_NURSES),
    'multistate_license': np.random.choice([True,False],N_NURSES,p=[.35,.65]),
    'full_time': np.random.choice([True,False],N_NURSES,p=[.72,.28]),
    'hire_date': [datetime(2008,1,1) + timedelta(days=random.randint(0, 16*365)) for _ in range(N_NURSES)],
})

# 2. shifts.csv - Timeline, schedule, workload
shifts_list = []
for nurse in nurses['nurse_id']:
    for week in range(40,53):    # simulate last 3 months only for CPU/time
        dt = datetime(2025,1,1) + timedelta(weeks=week)
        for s in range(np.random.choice([3,4,5,6])):
            t0 = dt + timedelta(days=random.choice(range(7)), hours=random.choice([7,19]))
            shifts_list.append({
                'shift_id':f"S{nurse}-{t0:%j%H}",
                'nurse_id':nurse,
                'date':t0.date(),
                'unit':np.random.choice(['ICU','Surgery','Medical','ED','Peds']),
                'shift_type':np.random.choice(['Day','Evening','Night'],p=[.45,.12,.43]),
                'hours': np.random.choice([8,10,12], p=[.21,.08,.71]),
                'patients': np.random.randint(2,9),
                'acuity': np.random.randint(1,11),
                'admissions': np.random.poisson(1.1),
                'discharges': np.random.poisson(0.7),
                'overtime': random.random()<0.09,
                'call_in': random.random()<0.04,
            })
shifts = pd.DataFrame(shifts_list)

# 3. nurses_feedback.csv - Self-reported wellbeing per shift
nurses_feedback = shifts.sample(frac=0.6).copy()
nurses_feedback['feedback_id'] = [f"F{i+1}" for i in range(len(nurses_feedback))]
nurses_feedback['reported_stress'] = np.random.choice(['Low','Medium','High'],len(nurses_feedback),p=[.38,.41,.21])
nurses_feedback['reported_fatigue'] = np.random.choice(['None','Moderate','Severe'],len(nurses_feedback),p=[.33,.53,.14])
nurses_feedback['burnout_freq'] = np.random.choice(['Never','Monthly','Weekly','Every day'],len(nurses_feedback),p=[.19,.19,.27,.35])
nurses_feedback['emotionally_drained'] = np.random.choice([True,False],len(nurses_feedback),p=[.18,.82])
nurses_feedback['used_up'] = np.random.choice([True,False],len(nurses_feedback),p=[.23,.77])
nurses_feedback['workload_change'] = np.random.choice(['More','No change','Less'],len(nurses_feedback),p=[.53,.37,.10])
nurses_feedback['intent_to_leave'] = np.random.choice([True,False],len(nurses_feedback),p=[.33,.67])
nurses_feedback['satisfaction'] = np.random.randint(1, 6, size=len(nurses_feedback))
nurses_feedback['comments'] = ""

# 4. supervisors_feedback.csv - Objective/external feedback
supervisors_feedback = nurses_feedback.sample(frac=0.45).copy()
supervisors_feedback['supervisor_id'] = [f"SUP{random.randint(1, N_SUPERVISORS)}" for _ in range(len(supervisors_feedback))]
supervisors_feedback['performance_score'] = np.random.randint(2,6,len(supervisors_feedback))
supervisors_feedback['reliability'] = np.random.choice(['Below avg','Average','Good','Excellent'],len(supervisors_feedback),p=[.06,.27,.39,.28])
supervisors_feedback['teamwork'] = np.random.choice(['Low','Moderate','High'],len(supervisors_feedback),p=[.06,.35,.59])
supervisors_feedback['clinical_decision'] = np.random.choice(['Appropriate','Needs improvement','Outstanding'],len(supervisors_feedback),p=[.69,.15,.16])
supervisors_feedback['remarks'] = ""

# 5. health.csv - Health (including absence/leave, incident)
health_list = []
for idx, nurse in nurses.iterrows():
    for m in range(random.randint(0,4)):
        absence_start = nurses['hire_date'].iloc[idx] + timedelta(days=random.randint(100,6000))
        ndays = random.choice([1,2,3,5,7,14])
        health_list.append({
            'record_id':f"HL{idx:04d}{m+1}",
            'nurse_id':nurse.nurse_id,
            'date': absence_start,
            'health_status': np.random.choice(['Healthy','Sick','Injured','Exhausted'],p=[.82,.12,.02,.04]),
            'absence_type': np.random.choice(['None','Sick leave','Vacation','Family','Health incident'],p=[.63,.18,.13,.05,.01]),
            'days_off': ndays,
            'return_date': absence_start + timedelta(days=ndays)
        })
health = pd.DataFrame(health_list)

# 6. pay.csv - Detailed compensation
pay = nurses[['nurse_id','primary_setting','specialty','education_nurse','full_time']].copy()
pay['annual_salary'] = (np.random.normal(88500,17000,len(pay))*(pay.full_time.map({True:1,False:.60}))).astype(int)
pay['overtime_rate'] = np.random.uniform(1.1,1.8,len(pay))
pay['bonus'] = np.random.choice([0,500,900,1800], len(pay), p=[.64,.21,.1,.05])

# 7. telehealth.csv - Technology adoption
telehealth = nurses[['nurse_id']].copy()
telehealth['used_telehealth'] = np.random.choice([True,False],len(telehealth),p=[.22,.78])
telehealth['mode'] = np.where(telehealth['used_telehealth'], np.random.choice(['Phone','Video','Text','Mixed'],len(telehealth)), "")

# 8. training.csv - Ongoing training/education
trainings = []
modules = ['Resilience','Infection control','Ethics','Leadership','Tech','Patient Safety','Emergency Response']
for idx, nurse in nurses.iterrows():
    for m in np.random.choice(modules, random.randint(1,4), replace=False):
        trainings.append({
            'training_id':f"T{idx+1}{m[0:2].upper()}",
            'nurse_id':nurse.nurse_id,
            'date': nurse.hire_date + timedelta(days=random.randint(300,5500)),
            'module': m,
            'completed': random.random()>0.07,
            'cert_expiry': datetime(2026,12,31) + timedelta(days=random.randint(0,720)),
        })
training = pd.DataFrame(trainings)

# 9. practice_multistate.csv - Multistate practice info
practice_multistate = nurses[['nurse_id','multistate_license']].copy()
practice_multistate['used_multistate_license'] = np.where(practice_multistate['multistate_license'], np.random.choice([True,False],len(practice_multistate)), False)
practice_multistate['purpose'] = np.where(practice_multistate['used_multistate_license'], np.random.choice(['Telehealth','Education','Disaster response','Other'],len(practice_multistate)), "")

# Save to CSV
nurses.to_csv("nurses_data_v3/nurses.csv",index=False)
shifts.to_csv("nurses_data_v3/shifts.csv",index=False)
nurses_feedback.to_csv("nurses_data_v3/nurses_feedback.csv",index=False)
supervisors_feedback.to_csv("nurses_data_v3/supervisors_feedback.csv",index=False)
health.to_csv("nurses_data_v3/health.csv",index=False)
pay.to_csv("nurses_data_v3/pay.csv",index=False)
telehealth.to_csv("nurses_data_v3/telehealth.csv",index=False)
training.to_csv("nurses_data_v3/training.csv",index=False)
practice_multistate.to_csv("nurses_data_v3/practice_multistate.csv",index=False)

print("\n✓ All files written:")
print(" - nurses.csv")
print(" - shifts.csv")
print(" - nurses_feedback.csv")
print(" - supervisors_feedback.csv")
print(" - health.csv")
print(" - pay.csv")
print(" - telehealth.csv")
print(" - training.csv")
print(" - practice_multistate.csv")
