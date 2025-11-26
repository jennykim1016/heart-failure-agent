import os
import sys
sys.path.append("/content/genie-worksheets/src/")
from pathlib import Path
from env_setting import env_content, env_content_dict

PROJECT_ROOT = Path("/Users/jennykim/Desktop/cs224v-project/genie-worksheets")
os.chdir(PROJECT_ROOT)

from worksheets.specification.from_spreadsheet import gsheet_to_classes

from openai import AzureOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

client = AzureOpenAI(
    api_version=env_content_dict['LLM_API_VERSION'],
    azure_endpoint=env_content_dict['LLM_API_ENDPOINT'],
    api_key=env_content_dict['LLM_API_KEY'],
)

import os
import requests
import zipfile
import shutil
from pathlib import Path
from io import BytesIO
from pathlib import Path

## Gemini-generated
def create_env_file():
    """
    Writes the environment variable content to a .env file 
    in the specified project directory.
    """
    
    # 1. Determine the Project Root Path
    # Assumes the script is run from the directory containing the 'genie-worksheets' folder
    current_dir = Path(os.getcwd())
    
    # Construct the full path to the .env file (e.g., /path/to/project/genie-worksheets/.env)
    env_file_path = current_dir / ".env"
    
    # Ensure the target directory (genie-worksheets) exists before writing
    # This is a good practice, though it likely already exists from previous steps
    env_file_path.parent.mkdir(parents=True, exist_ok=True) 

    # 2. Write the Content to the File
    # This block is the direct translation of your original 'with open' statement
    with open(env_file_path, "w") as f:
      f.write(env_content)

    print(f"Environment file successfully written to: {env_file_path}")

## Gemini-generated
def setup_credentials():
    """
    Handles downloading, unzipping, and moving credential files 
    for the genie-worksheets project.
    """
    # --- 1. Define Paths (Equivalent to os.getcwd() and os.path.join()) ---
    
    # Use Path for modern, OS-agnostic path handling
    current_dir = Path(os.getcwd())
    
    # Define the target subdirectory for the final credential files
    config_dir = current_dir / "src" / "worksheets" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    # --- 2. Download and Unzip (Equivalent to !curl and !unzip) ---
    
    DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id=11QvSs2JZ5qpPrCvbX66Dg8pxfM_B8GaH"
    TEMP_ZIP_NAME = "creds.zip"

    print(f"Starting download to temporary file: {TEMP_ZIP_NAME}")
    
    try:
        # Download the zip file content
        response = requests.get(DOWNLOAD_URL, stream=True)
        response.raise_for_status() 
        
        # Save the content to a temporary file in the current directory
        temp_zip_path = current_dir / TEMP_ZIP_NAME
        with open(temp_zip_path, 'wb') as f:
            f.write(response.content)

        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            # Extract contents directly into the project directory
            zip_ref.extractall(current_dir)
        
        # Clean up the temporary zip file
        os.remove(temp_zip_path)
        print("Download and extraction complete.")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Download failed. {e}")
        return
    except zipfile.BadZipFile:
        print("ERROR: Downloaded file is not a valid zip file.")
        return

    # --- 3. Move Credential Files (Equivalent to !mv commands) ---
    
    # Define the files that were extracted (Source) and their final destination (Target)
    files_to_move = [
        "credentials.json",
        "service_account.json",
        "token.json"
    ]

    for filename in files_to_move:
        # The zip extracts files to current_dir/worksheets/filename
        # The original Colab path was /content/genie-worksheets/worksheets/filename
        source_path = current_dir / "worksheets" / filename
        
        # The destination path is current_dir/src/worksheets/config/filename
        # The original Colab destination was /content/genie-worksheets/src/worksheets/config/filename
        target_path = config_dir / filename
        
        try:
            # shutil.move is the Python equivalent of the 'mv' command
            shutil.move(str(source_path), str(target_path))
            print(f"Moved {filename} successfully.")
        except FileNotFoundError:
            print(f"WARNING: Source file not found: {source_path}. Skipping move.")

    # --- 4. Assertion/Verification (Equivalent to the assert block) ---
    
    # The paths are already defined above, but we redefine them using Path for clarity
    creds_paths = [
        config_dir / "credentials.json",
        config_dir / "service_account.json",
        config_dir / "token.json"
    ]

    print("\nVerifying file existence...")
    for cred_path in creds_paths:
        assert cred_path.exists(), f"Cannot find the credential file: {cred_path}"
        print(f"Verified: {cred_path.name}")

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Say 'hi.'",
        }
    ],
    model="gpt-4.1"
)

create_env_file()
setup_credentials()

print(response.choices[0].message.content)

from enum import Enum

class DailyDose(Enum):
  ONCE_PER_DAY = 1
  TWICE_PER_DAY = 2
  THREE_TIMES_PER_DAY = 3

dose_daily_guidance = {
    DailyDose.ONCE_PER_DAY: 'PO daily',
    DailyDose.TWICE_PER_DAY: 'PO twice daily',
    DailyDose.THREE_TIMES_PER_DAY: 'three times daily',
}

dose_guidance = {
    # medication name: [[mg doses], occurences]
    'enalapril': [[2.5, 5, 10, 20], DailyDose.TWICE_PER_DAY], # ACE
    'lisinopril': [[2.5, 5, 10, 20, 40], DailyDose.ONCE_PER_DAY], # ACE
    'ramipril': [[1.25, 2.5, 5, 10], DailyDose.ONCE_PER_DAY], # ACE
    'captopril': [[6.25, 12.5, 25, 50], DailyDose.THREE_TIMES_PER_DAY], # ACE
    'losartan': [[25, 50, 100], DailyDose.ONCE_PER_DAY], # ARB
    'valsartan': [[40, 80, 160], DailyDose.TWICE_PER_DAY], # ARB
    'candesartan': [[4, 8, 16, 32, DailyDose.ONCE_PER_DAY]], # ARB
    # skipped ARNI
    'spironolactone': [[12.5, 25, 50], DailyDose.ONCE_PER_DAY], # Aldosteron Antagonist
    'eplerenone': [[25, 50], DailyDose.ONCE_PER_DAY], # Aldosteron Antagonist
    'carvedilol': [[3.125, 6.25, 12.5, 25], DailyDose.TWICE_PER_DAY], # Beta Blocker
    'metoprolol succinate': [[12.5, 25, 50, 100, 200], DailyDose.ONCE_PER_DAY], # Beta Blocker
    'bisoprolol': [[1.25, 2.5, 5, 10], DailyDose.ONCE_PER_DAY], # Beta Blocker
}

import json

def is_angioedema(user_prompt):
    """Check for angioedema symptoms."""
    if not user_prompt or user_prompt.lower() in ['none', 'no', 'n/a', '']:
        return False

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a medical symptom classifier. Determine if the patient's symptoms indicate angioedema.

                Angioedema symptoms include:
                - Swelling of lips, tongue, face, throat, or eyelids
                - Puffiness in facial areas
                - Any mention of swelling in these specific areas

                Return ONLY a valid JSON object with format: {"angioedema": "Yes"} or {"angioedema": "No"}

                Examples:
                - "swollen lips and tongue" → {"angioedema": "Yes"}
                - "my eyelids are puffy" → {"angioedema": "Yes"}
                - "feeling tired" → {"angioedema": "No"}
                - "altered mental state" → {"angioedema": "No"}"""
            },
            {
                "role": "user",
                "content": f"Patient symptoms: {user_prompt}"
            }
        ],
        model="gpt-4.1",
        temperature=0.0  # Use 0 for deterministic classification
    )

    try:
        json_string = response.choices[0].message.content
        # Remove markdown code blocks if present
        json_string = json_string.replace('```json', '').replace('```', '').strip()
        data = json.loads(json_string)
        return data.get('angioedema', 'No') == 'Yes'
    except Exception as e:
        print(f"Error in is_angioedema: {e}, response: {json_string}")
        # If unsure, err on the side of caution
        return False

def is_bronchospasm(user_prompt):
    """Check for bronchospasm symptoms."""
    if not user_prompt or user_prompt.lower() in ['none', 'no', 'n/a', '']:
        return False

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a medical symptom classifier. Determine if the patient's symptoms indicate bronchospasm or respiratory distress.

                Bronchospasm symptoms include:
                - Difficulty breathing, shortness of breath, gasping for air
                - Wheezing or chest tightness
                - Cannot speak in full sentences due to breathlessness
                - Running out of breath
                - Chest spasm or tightness related to breathing

                Return ONLY a valid JSON object with format: {"BS": "Yes"} or {"BS": "No"}

                Examples:
                - "gasping for breath, can't speak in full sentences" → {"BS": "Yes"}
                - "chest tightness and wheezing" → {"BS": "Yes"}
                - "feeling tired" → {"BS": "No"}
                - "swollen lips" → {"BS": "No"}"""
            },
            {
                "role": "user",
                "content": f"Patient symptoms: {user_prompt}"
            }
        ],
        model="gpt-4.1",
        temperature=0.0
    )

    try:
        json_string = response.choices[0].message.content
        json_string = json_string.replace('```json', '').replace('```', '').strip()
        data = json.loads(json_string)
        return data.get('BS', 'No') == 'Yes'
    except Exception as e:
        print(f"Error in is_bronchospasm: {e}")
        return False

def is_adhf(user_prompt):
    """Check for acute decompensated heart failure symptoms."""
    if not user_prompt or user_prompt.lower() in ['none', 'no', 'n/a', '']:
        return False

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a medical symptom classifier. Determine if the patient's symptoms indicate acute decompensated heart failure (ADHF) requiring urgent medical attention.

                ADHF symptoms include:
                - Altered mental status, confusion, disorientation
                - Severe shortness of breath or gasping
                - Inability to speak in full sentences
                - Extreme fatigue or weakness
                - Signs of fluid overload (severe swelling, difficulty breathing when lying down)

                Return ONLY a valid JSON object with format: {"ADHF": "Yes"} or {"ADHF": "No"}

                Examples:
                - "altered mental state, confused, forgetful" → {"ADHF": "Yes"}
                - "brain feels foggy, confused, can't think" → {"ADHF": "Yes"}
                - "gasping for breath, can't speak full sentences, confused" → {"ADHF": "Yes"}
                - "feeling a bit tired" → {"ADHF": "No"}
                - "swollen ankles" → {"ADHF": "No"}"""
            },
            {
                "role": "user",
                "content": f"Patient symptoms: {user_prompt}"
            }
        ],
        model="gpt-4.1",
        temperature=0.0
    )

    try:
        json_string = response.choices[0].message.content
        json_string = json_string.replace('```json', '').replace('```', '').strip()
        data = json.loads(json_string)
        return data.get('ADHF', 'No') == 'Yes'
    except Exception as e:
        print(f"Error in is_adhf: {e}")
        return False

def is_gynecomastia(user_prompt, is_male):
    """Check for gynecomastia symptoms."""
    if not is_male or not user_prompt or user_prompt.lower() in ['none', 'no', 'n/a', '']:
        return False

    user_prompt_with_gender = f"{user_prompt} I am a male."

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a medical symptom classifier. Determine if the male patient's symptoms indicate gynecomastia.

                Gynecomastia symptoms in males include:
                - Enlarged breasts or breast tissue
                - Breast tenderness or pain
                - Swelling in breast area

                Return ONLY a valid JSON object with format: {"gynecomastia": "Yes"} or {"gynecomastia": "No"}

                Examples:
                - "enlarged breast and breast tenderness" → {"gynecomastia": "Yes"}
                - "chest pain from injury" → {"gynecomastia": "No"}
                - "swollen lips" → {"gynecomastia": "No"}"""
            },
            {
                "role": "user",
                "content": f"Patient symptoms: {user_prompt_with_gender}"
            }
        ],
        model="gpt-4.1",
        temperature=0.0
    )

    try:
        json_string = response.choices[0].message.content
        json_string = json_string.replace('```json', '').replace('```', '').strip()
        data = json.loads(json_string)
        return data.get('gynecomastia', 'No') == 'Yes'
    except Exception as e:
        print(f"Error in is_gynecomastia: {e}")
        return False

from worksheets.agent.config import agent_api

@agent_api("is_ace_inhibitor", "Checks whether the given medication is an ACE inhibitor.")
def is_ace_inhibitor(medication):
    med_str = str(medication).strip().lower()
    return med_str in ['enalapril', 'lisinopril', 'ramipril', 'captopril']


@agent_api("is_arb_inhibitor", "Checks whether the given medication is an ARB inhibitor.")
def is_arb_inhibitor(medication):
    med_str = str(medication).strip().lower()
    return med_str in ['losartan', 'valsartan', 'candesartan']


@agent_api("is_aldosteron_antagonist", "Checks whether the given medication is an aldosterone antagonist.")
def is_aldosteron_antagonist(medication):
    med_str = str(medication).strip().lower()
    return med_str in ['spironolactone', 'eplerenone']

@agent_api("is_beta", "Checks whether the given medication is a beta blocker.")
def is_beta(medication):
    med_str = str(medication).lower()
    return med_str in ['carvedilol', 'metoprolol succinate', 'bisoprolol']

# common vital sign checks, common across all medications.

@agent_api("check_medication_vital_sign", "Generates the titration plan for the patient given the vital signs.")
def check_medication_vital_sign(medication_name, medication_dose, systolic_blood_pressure, diastolic_blood_pressure, heart_rate_per_min):
  if systolic_blood_pressure > 200 or systolic_blood_pressure < 80 or diastolic_blood_pressure > 110 or diastolic_blood_pressure < 40:
    return {
        'response': 'Your blood pressure is not in the normal range. Please contact your physician and hold the medication for now.',
        'continue': False,
    }
  if heart_rate_per_min < 50:
    return {
        'response': 'Your heart rate is low (<50 bpm). Please contact your physician and hold the medication for now.',
        'continue': False,
    }
  return {
      'response': 'I need some more information.',
      'continue': True,
  }

import random
from uuid import uuid4
import bisect

@agent_api("check_medication_ace_arb", "Generates the titration plan for the patient who is taking an ACE or ARB inhibitor.")
def check_medication_ace_arb(medication_name, medication_dose, potassium, e_gfr, percentage_creatinine_increase, noticeable_symptoms):
  stop_cause = ''
  stop = False
  nonexisting_lab = []

  if potassium:
    if potassium > 5.5:
      stop_cause += f'Your potassium is {potassium} mEq/L, which is above the safe limit. Hold the medication and recheck labs before resuming.'
      stop = True
  else:
    nonexisting_lab.append('Potassium')
  if e_gfr:
    if e_gfr < 30:
      if stop_cause:
        stop_cause += ' '
      stop_cause += f'eGFR is {e_gfr} mL/min. You may need to discontinue the medication. Contact your physician before continuing.'
      stop = True
  else:
    nonexisting_lab.append('eGFR')
  if percentage_creatinine_increase:
    if percentage_creatinine_increase > 30:
      if stop_cause:
        stop_cause += ' '
      stop_cause += f'Your percentage creatinine increase is {percentage_creatinine_increase}%. This is above 30%, which suggests you should hold the medication.'
      stop = True
  else:
    nonexisting_lab.append('% Creatinine')
  # hyperkalemia_intervention: ignore for now as we check the potassium level
  # systolic blood pressure: ignore for now as we check the vital sign above
  if is_angioedema(str(noticeable_symptoms)):
    if stop_cause:
      stop_cause += ' '
    stop_cause += 'Angioedema is a contraindication. Stop the medication immediately and seek medical attention.'
    stop = True
  if stop:
    return {
        'response': stop_cause,
    }

  initial_response = ", ".join(nonexisting_lab) + " are missing, but we will give the titration guideline with assuming these labs do not indicate anything problematic."

  medication_name = medication_name.lower()
  index = bisect.bisect_right(dose_guidance[medication_name][0], medication_dose)
  target_index = index + 1 # increase the titration dose
  if target_index >= len(dose_guidance[medication_name][0]) - 1:
    return {
        'response': initial_response + 'You are already taking the maximum dose, please continue the current dose and let us know immediately if you see any unexpected symptoms.',
    }
  return {
      'response': initial_response + 'Let\'s increase your dose. Please start taking ' + str(dose_guidance[medication_name][0][target_index]) + ' ' + str(dose_daily_guidance[dose_guidance[medication_name][1]]) + ' and let us know immediately if you see any unexpected symptoms.'
  }

import random
from uuid import uuid4
import bisect

@agent_api("check_medication_aa", "Generates the titration plan for the patient who is taking an Aldosterone Antagonist.")
def check_medication_aa(medication_name, medication_dose, potassium, e_gfr, percentage_creatinine_increase, noticeable_symptoms, is_male):
  stop_cause = ''
  stop = False
  nonexisting_lab = []

  if potassium:
    if potassium > 5.5:
      stop_cause += f'Your potassium is {potassium} mEq/L, which is above the safe limit. Hold the medication and recheck labs before resuming.'
      stop = True
  else:
    nonexisting_lab.append('Potassium')
  if e_gfr:
    if e_gfr < 30:
      if stop_cause:
        stop_cause += ' '
      stop_cause += f'eGFR is {e_gfr} mL/min. You may need to discontinue the medication. Contact your physician before continuing.'
      stop = True
  else:
    nonexisting_lab.append('eGFR')
  if percentage_creatinine_increase:
    if percentage_creatinine_increase > 30:
      if stop_cause:
        stop_cause += ' '
      stop_cause += f'Your percentage creatinine increase is {percentage_creatinine_increase}%. This is above 30%, which suggests you should hold the medication.'
      stop = True
  else:
    nonexisting_lab.append('% Creatinine')
  if is_gynecomastia(str(noticeable_symptoms, is_male)):
    if stop_cause:
      stop_cause += ' '
    stop_cause += 'You seem to have a Gynecomastia, and it is a contraindication. Stop the medication immediately and seek medical attention.'
    stop = True
  if has_breast_tenderness(str(noticeable_symptoms)):
    if stop_cause:
      stop_cause += ' '
    stop_cause += 'You seem to have breast tenderness, and it is a contraindication. Stop the medication immediately and seek medical attention.'
    stop = True
  if stop:
    return {
        'response': stop_cause,
    }

  initial_response = ", ".join(nonexisting_lab) + "are missing, but we will give the titration guideline with assuming these labs do not indicate anything problematic. "

  medication_name = medication_name.lower()
  index = bisect.bisect_right(dose_guidance[medication_name][0], medication_dose)
  target_index = index + 1 # increase the titration dose
  if target_index >= len(dose_guidance[medication_name][0]) - 1:
    return {
        'response': initial_response + 'You are already taking the maximum dose, please continue the current dose and let us know immediately if you see any unexpected symptoms.',
    }
  return {
      'response': initial_response + 'Let\'s increase your dose. Please start taking ' + str(dose_guidance[medication_name][0][target_index]) + ' ' + str(dose_daily_guidance[dose_guidance[medication_name][1]]) + ' and let us know immediately if you see any unexpected symptoms.',
  }

import bisect

@agent_api("check_medication_beta", "Generates the titration plan for the patient who is taking a Beta Blocker.")
def check_medication_beta(medication_name, medication_dose, heart_rate, systolic_bp, weight_kg, noticeable_symptoms):
    """
    Parameters:
      medication_name: str - Beta blocker name
      medication_dose: float - current dose in mg
      heart_rate: int - current heart rate in bpm
      systolic_bp: int - systolic blood pressure (optional, for warnings)
      weight_kg: float - patient's weight in kg (optional, for Carvedilol dosing)
      noticeable_symptoms: str - patient-reported symptoms
    """
    medication_name_lower = medication_name.lower()

    if medication_name_lower not in dose_guidance:
        return {'response': f"Unknown medication {medication_name}. Cannot provide titration guidance."}

    # Check for contraindications - STOP conditions
    stop_messages = []

    # Check for bronchospasm (CRITICAL contraindication for beta-blockers)
    if is_bronchospasm(str(noticeable_symptoms)):
        stop_messages.append("You are experiencing bronchospasm or severe breathing difficulty. This is a contraindication for beta-blockers. Stop the medication immediately and seek emergency medical attention.")

    # Check for ADHF (CRITICAL - altered mental status, confusion)
    if is_adhf(str(noticeable_symptoms)):
        stop_messages.append("You are experiencing symptoms of acute decompensated heart failure (altered mental status or confusion). Stop the medication immediately and seek emergency medical attention. You may require IV diuretics or inotropes.")

    # Check heart rate
    if heart_rate < 45:
        stop_messages.append(f"Your heart rate is {heart_rate} bpm, which is critically low (below 45 bpm). Hold the medication and contact your physician immediately. You may need to discontinue or reduce your dose.")
    elif heart_rate < 50:
        stop_messages.append(f"Your heart rate is {heart_rate} bpm, which is too low (below 50 bpm). Hold the medication and contact your physician before taking your next dose.")

    # Check systolic blood pressure
    if systolic_bp and systolic_bp < 85:
        stop_messages.append(f"Your systolic blood pressure is {systolic_bp} mmHg, which is too low. Hold the medication and contact your physician.")

    # If any critical warning applies, return immediately
    if stop_messages:
        return {'response': " ".join(stop_messages)}

    # Determine next titration dose
    doses = dose_guidance[medication_name_lower][0]
    unit = dose_daily_guidance[dose_guidance[medication_name_lower][1]]

    # Determine maximum allowable dose based on weight for Carvedilol
    if medication_name_lower == "carvedilol" and weight_kg:
        if weight_kg > 85:
            max_dose = 50.0
        else:
            max_dose = 25.0
        # Find the index of max_dose in the doses list
        try:
            max_index = doses.index(max_dose)
        except ValueError:
            max_index = len(doses) - 1
    else:
        max_index = len(doses) - 1

    # Find current dose position
    current_index = bisect.bisect_left(doses, medication_dose)

    # Check if already at or above max dose
    if current_index >= max_index:
        return {
            'response': f"You are already taking the maximum recommended dose of {medication_name.capitalize()} for your weight ({medication_dose}mg {unit}). Continue the current dose and monitor your heart rate and blood pressure. Let us know immediately if you see any unexpected symptoms."
        }

    # Calculate next dose (one step up)
    next_index = current_index + 1

    # Make sure we don't exceed max
    if next_index > max_index:
        next_index = max_index

    next_dose = doses[next_index]

    # Check if we're actually increasing (shouldn't happen given above logic, but safe check)
    if next_dose <= medication_dose:
        return {
            'response': f"You are already at the target dose of {medication_name.capitalize()} ({medication_dose}mg {unit}). Continue the current dose and monitor your heart rate and blood pressure. Let us know immediately if you see any unexpected symptoms."
        }

    return {
        'response': f"Based on your current information, let's increase your dose. Please start taking {medication_name.capitalize()} {next_dose}mg {unit} and monitor your heart rate and symptoms carefully. If you experience dizziness, extreme fatigue, shortness of breath, or if your heart rate drops below 50 bpm, contact your healthcare provider immediately."
    }

gsheet_id_default = "1ipfSs-7mqqnnI6ao_4Ohfr3bOSBozfNn4xzEiFv20R8"

botname = "Heart Failure Agent"
starting_prompt = "Hi, welcome to the Heart Failure Medication Titration Service! I'm here to help review your heart failure medication and make recommendations. What is your name?"
description = """
You are a Heart Failure Medication Titration Agent. Your goal is to gather information from patients and provide safe, appropriate medication titration recommendations.

CRITICAL INFORMATION YOU MUST COLLECT:
1. Patient's full name
2. Biological gender (male/female) - required for accurate dosing
3. Current medication name and exact dose (including frequency: daily, twice daily, etc.)
4. Vital signs: systolic and diastolic blood pressure, heart rate
5. Relevant lab results: potassium level, creatinine changes
6. Current symptoms or side effects
7. Weight (for dosing calculations)

CONVERSATION GUIDELINES:
- Address the patient directly using "you" (not third person)
- Be warm, friendly, and conversational while remaining professional
- Handle confused or difficult patients with patience and clarity
- When patients give conflicting information, gently seek clarification without being repetitive
- If patients provide information out of order, acknowledge it and continue naturally
- When patients change their answers, confirm the correct information: "Just to make sure I have this right, you're taking [medication] at [dose], correct?"
- If a patient seems uncertain about critical information (like medication dose), ask them to check their medication bottle or records
- Don't ask the same question multiple times unless absolutely necessary
- If a name is similar enough (Ben/Benjamin, Lisa/Elisabeth), accept it and move forward

SAFETY-FIRST APPROACH:
- NEVER make recommendations when you're missing critical information
- If you cannot get necessary information after reasonable attempts, explain what you need and why
- Always identify and flag contraindications and safety concerns
- Be appropriately cautious when information is unclear or contradictory

CONTRAINDICATIONS - MUST STOP MEDICATION:
- Angioedema (swelling of lips, tongue, face, throat)
- Potassium > 5.5 mEq/L
- Creatinine increase > 50% from baseline
- Bronchospasm with beta-blockers (shortness of breath, wheezing, difficulty breathing)
- Severe gynecomastia or breast tenderness with spironolactone
- Heart rate < 50 bpm with beta-blockers
- Altered mental status suggesting acute decompensated heart failure

If any contraindication is present, recommend STOPPING the medication immediately and seeking medical attention. Be clear and direct about the urgency.

TITRATION RECOMMENDATIONS:
- Only provide titration advice after collecting ALL necessary information
- If information is missing, explicitly state what you still need
- Base recommendations on the complete clinical picture
- When recommending dose changes, be specific about the new dose and frequency
- Explain to the patient that they should follow up with their healthcare provider

ENDING THE CONVERSATION:
- Provide a clear summary of your recommendation
- Ensure the patient understands the next steps
- If stopping medication, emphasize the importance of seeking immediate medical care
- If increasing dose, remind them to monitor for side effects
- Be prepared for the patient to say "exit" when ready to end the conversation

Remember: You are a helpful assistant providing recommendations, but always emphasize that patients should follow up with their healthcare provider. Your primary duty is patient safety.
"""

# Helper code to convert the dialogue state to JSON format

from worksheets.utils.annotation import get_agent_action_schemas, get_context_schema
from worksheets.core.dialogue import CurrentDialogueTurn

def convert_to_json(dialogue: list[CurrentDialogueTurn]):
    json_dialogue = []
    for turn in dialogue:
        user_utterance = turn.user_utterance
        system_response = turn.system_response
        context = turn.context
        global_context = turn.global_context
        system_action = turn.system_action
        user_target_sp = turn.user_target_sp
        user_target = turn.user_target
        user_target_suql = turn.user_target_suql
        json_turn = {
            "user": user_utterance,
            "bot": system_response,
            "turn_context": get_context_schema(context),
            "global_context": get_context_schema(global_context),
            "system_action": get_agent_action_schemas(system_action),
            "user_target_sp": user_target_sp,
            "user_target": user_target,
            "user_target_suql": user_target_suql,
        }
        json_dialogue.append(json_turn)
    return json_dialogue

# You need to define the models to use for each componenet of Genie Worksheets.
# You can also load the configurations from a yaml file.

from worksheets.agent.config import Config, AzureModelConfig

config = Config(
    semantic_parser = AzureModelConfig(
        model_name="azure/gpt-4.1",
    ),
    response_generator = AzureModelConfig(
        model_name="azure/gpt-4.1",
    ),
    knowledge_parser=AzureModelConfig(),
    knowledge_base=AzureModelConfig(),
    validate_response= False,

    prompt_log_path = "logs.log",
    conversation_log_path= "conv_log.json",
)

from worksheets.llm.prompts import init_llm

init_llm(
    str(PROJECT_ROOT / "src" / "worksheets" / "prompts"), # Path to the templates directory
    str(PROJECT_ROOT / ".env")                            # Path to the .env file
)

# Main agent builder that generates the agent for you
from worksheets import AgentBuilder, conversation_loop # utils.interface
import json
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="ERROR")

agent_builder = (
    AgentBuilder(
        name=botname,
        description=description,
        starting_prompt=starting_prompt
    )
    .with_gsheet_specification(gsheet_id_default)
)

agent = agent_builder.build(config)

for ws in agent.runtime.genie_worksheets:
  print(ws)

def get_patient_persona(patient):
  return f"""Your name is {patient["name"]}, and you are {patient["gender"]}.
  The heart failure medication titration agent will ask you questions.
  Please answer based on the information you have.
  You have a systolic blood pressure of {patient["systolic_blood_pressure"]} mmHg, and diastolic blood pressure of {patient["diastolic_blood_pressure"]}.
  Your heart rate is {patient["heart_rate_per_min"]} bpm.
  You are currently taking {patient["medication"]} {patient["dose"]}.
  While taking the medication, you have experienced the following side effects: {patient["side_effect"]}. You have the following lab results: {patient["lab_result"]}.
  Your weight is {patient["weight"]}.
  IMPORTANT: NEVER say just 'None' or refuse to answer. If you're confused, say something like 'I'm not sure, let me think...' or 'Can you ask that in a different way?' or give a confused answer with multiple possibilities.
  When you hear the titration guideline, please explicitly answer `exit` to finish the conversation."""

# Define patient config = array of {"name": name, "gender": m/f, "medication": medication, "dose": dose x times a day, "side effect": description of side effect, "lab result": lab result}
# TODO: define more patients
patient_sarah = {
    "name": "Sarah",
    "gender": "female",
    "medication": "Lisinopril", # ACE Inhibitors
    "dose": "5mg PO daily",
    "systolic_blood_pressure": 120,
    "diastolic_blood_pressure": 80,
    "heart_rate_per_min": 75,
    "side_effect": "swollen lips, tongue, and eyelids", # angioedema, stop condition
    "lab_result": "Potassium was 5.0mEq/L",
    "weight": "120 pounds"
}

patient_alex = {
    "name": "Alex",
    "gender": "male",
    "medication": "Metoprolol Succinate", # Beta Blockers
    "dose": "5mg PO daily",
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 90,
    "side_effect": "None",
    "lab_result": "Potassium was 5.0mEq/L",
    "weight": "250 pounds"
}

patient_steven = {
    "name": "Steven",
    "gender": "male",
    "medication": "Enalapril",
    "dose": "5mg PO daily", # ACE Inhibitors
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 90,
    "side_effect": "None",
    "lab_result": "Potassium was 6.0mEq/L", # potassium lab, stop condition
    "weight": "250 pounds"
}

patient_julie = {
    "name": "Julie",
    "gender": "female",
    "medication": "Enalapril",
    "dose": "5mg PO daily", # ACE Inhibitor
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 90,
    "side_effect": "None",
    "lab_result": "Creatinine increase was 50% from the baseline.", # creatinine lab increase, stop condition
    "weight": "250 pounds"
}

patient_cara = {
    "name": "Cara",
    "gender": "female",
    "medication": "Candesartan", # ARB Inhibitor
    "dose": "8mg PO daily",
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 90,
    "side_effect": "None",
    "lab_result": "Potassium was 3.0mEq/L",
    "weight": "140 pounds" # no side effect, increase to 16mg PO daily
}

patient_jim = {
    "name": "Jim",
    "gender": "male",
    "medication": "Spironolactone", # Aldosteron Antagonist
    "dose": "12.5mg PO daily",
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 40, # heart rate problematic
    "side_effect": "None",
    "lab_result": "Potassium was 6.0mEq/L", # Should also discontinue
    "weight": "170 pounds"
}

patient_jay = {
    "name": "Jay",
    "gender": "male",
    "medication": "Spironolactone", # Aldosteron Antagonist
    "dose": "12.5mg PO daily",
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 60,
    "side_effect": "None",
    "lab_result": "Potassium was 6.0mEq/L", # Should discontinue
    "weight": "170 pounds"
}

patient_julius = {
    "name": "Julius",
    "gender": "male",
    "medication": "Spironolactone", # Aldosteron Antagonist
    "dose": "12.5mg PO daily",
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 60,
    "side_effect": "Had a enlarged breast and breast tenderness", # Severe gynecomastia and breast tenderness
    "lab_result": "Potassium was 4.0mEq/L",
    "weight": "170 pounds"
}

patient_brian = {
    "name": "Brian",
    "gender": "male",
    "medication": "Carvedilol", # Beta Blocker, bronchospasm, stop
    "dose": "12.5mg PO daily",
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 60,
    "side_effect": "I am experiencing an inability to speak in full sentences and gasping for breath. I am always so confused and not able to think, while running out of breadth.",
    "lab_result": "Potassium was 4.0mEq/L",
    "weight": "170 pounds"
}

patient_ben = {
    "name": "Ben",
    "gender": "male",
    "medication": "Carvedilol", # Beta Blocker, potential acute decompensated heart failure that can require IV diuretics / inotropes, stop
    "dose": "12.5mg PO daily",
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 60,
    "side_effect": "I am experiencing altered mental state.",
    "lab_result": "Potassium was 4.0mEq/L",
    "weight": "170 pounds"
}

patient_jamie = {
    "name": "Jamie",
    "gender": "male",
    "medication": "Carvedilol", # Beta Blocker, no side effect, increase to 25mg
    "dose": "12.5mg PO daily",
    "systolic_blood_pressure": 130,
    "diastolic_blood_pressure": 90,
    "heart_rate_per_min": 60,
    "side_effect": "",
    "lab_result": "Potassium was 4.0mEq/L",
    "weight": "170 pounds"
}

patient_lisa = {
    "name": "Lisa",
    "gender": "female",
    "medication": "Lisinopril", # ACE Inhibitor, all good, increase to 2.5mg (linear interpolation may be needed)
    "dose": "2.5mg PO daily",
    "systolic_blood_pressure": 120,
    "diastolic_blood_pressure": 80,
    "heart_rate_per_min": 75,
    "side_effect": "I am experiencing an altered mental state. I am experiencing bronchospasm", # not a stop condition for ACE Inhibitor
    "lab_result": "Potassium was 3.0mEq/L",
    "weight": "120 pounds"
}

patient_judy = {
    "name": "Judy",
    "gender": "female",
    "medication": "Lisinopril", # ACE Inhibitor, all good, increase to 2.5mg
    "dose": "2.5mg PO daily",
    "systolic_blood_pressure": 120,
    "diastolic_blood_pressure": 80,
    "heart_rate_per_min": 75,
    "side_effect": "no side effect or symptoms",
    "lab_result": "Potassium was 3.0mEq/L",
    "weight": "120 pounds"
}

# patients_array = [patient_sarah, patient_alex, patient_steven, patient_julie, patient_cara, patient_jim, patient_jay, patient_julius, patient_brian, patient_ben, patient_jamie]
patients_array = [patient_ben, patient_lisa, patient_brian, patient_sarah]

from openai import AzureOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv(dotenv_path='/content/genie-worksheets/.env')

patient_client = AzureOpenAI(
    api_version=os.getenv("LLM_API_VERSION"),
    azure_endpoint=os.getenv("LLM_API_ENDPOINT"),
    api_key=os.getenv("LLM_API_KEY"),
)

def get_patient_response(client, conversation_history):
    try:
        # Call the Chat Completion API
        response = client.chat.completions.create(
            model="gpt-4.1", # Use your deployment name
            messages=conversation_history,
        )

        # Extract the model's response
        chatbot_reply = response.choices[0].message.content
        return chatbot_reply

    except Exception as e:
        return f"An error occurred: {e}"

def get_patient_persona_hard(patient):
  return f"""Your name is {patient["name"]}, and you are {patient["gender"]}.
  The heart failure medication titration agent will ask you questions.
  Please answer based on the information you have.
  You have a systolic blood pressure of {patient["systolic_blood_pressure"]} mmHg, and diastolic blood pressure of {patient["diastolic_blood_pressure"]}.
  Your heart rate is {patient["heart_rate_per_min"]} bpm.
  You are currently taking {patient["medication"]} {patient["dose"]}.
  While taking the medication, you have experienced the following side effects: {patient["side_effect"]}. You have the following lab results: {patient["lab_result"]}.
  Your weight is {patient["weight"]}.
  Try to be a bit difficult and confusing to the agent, while still managing to get the conversation done to really test the agent on whether it can handle problamatic patients.
  IMPORTANT: NEVER say just 'None' or refuse to answer. If you're confused, say something like 'I'm not sure, let me think...' or 'Can you ask that in a different way?' or give a confused answer with multiple possibilities.
  When you hear the titration guideline, please explicitly answer `exit` to finish the conversation."""

def get_patient_persona_hardest(patient):
  return f"""Your name is {patient["name"]}, and you are {patient["gender"]}.
  The heart failure medication titration agent will ask you questions.
  Please answer based on the information you have.
  You have a systolic blood pressure of {patient["systolic_blood_pressure"]} mmHg, and diastolic blood pressure of {patient["diastolic_blood_pressure"]}.
  Your heart rate is {patient["heart_rate_per_min"]} bpm.
  You are currently taking {patient["medication"]} {patient["dose"]}.
  While taking the medication, you have experienced the following side effects: {patient["side_effect"]}. You have the following lab results: {patient["lab_result"]}.
  Your weight is {patient["weight"]}.
  Try to be a bit difficult and confusing to the agent, while still managing to get the conversation done to really test the agent on whether it can handle problamatic patients.
  Try answering with your medicine, numbers, etc. wrong, then once the medical assistent moves on, go back and be like 'actually it was this'.
  IMPORTANT: NEVER say just 'None' or refuse to answer. If you're confused, say something like 'I'm not sure, let me think...' or 'Can you ask that in a different way?' or give a confused answer with multiple possibilities.
  When you hear the titration guideline, please explicitly answer `exit` to finish the conversation."""

import json
import re
from typing import Dict, List, Any

def format_conversation(conversation_history):
    """Format conversation history for the evaluator."""
    formatted = []
    for turn in conversation_history:
        role = turn["role"]
        content = turn["content"]
        if role == "system":
            continue  # Skip system messages
        elif role == "user":
            formatted.append(f"AGENT: {content}")
        elif role == "assistant":
            formatted.append(f"PATIENT: {content}")
    return "\n\n".join(formatted)

def get_evaluator_prompt(conversation_history, patient_data):
    return f"""You are an expert evaluator assessing a heart failure medication titration conversation between an AI agent and a patient.

PATIENT GROUND TRUTH DATA:
- Name: {patient_data["name"]}
- Gender: {patient_data["gender"]}
- Medication: {patient_data["medication"]} {patient_data["dose"]}
- Blood Pressure: {patient_data["systolic_blood_pressure"]}/{patient_data["diastolic_blood_pressure"]} mmHg
- Heart Rate: {patient_data["heart_rate_per_min"]} bpm
- Side Effects: {patient_data["side_effect"]}
- Lab Results: {patient_data["lab_result"]}
- Weight: {patient_data["weight"]}

CONVERSATION TRANSCRIPT:
{format_conversation(conversation_history)}

Please evaluate this conversation on the following criteria and provide scores from 1-5 (where 1 is poor and 5 is excellent):

1. **Information Gathering Completeness** (1-5):
   - Did the agent successfully collect all necessary information (name, gender, medication, dose, vital signs, labs, symptoms)?
   - Score: [1-5]
   - Missing information: [list any critical data points not collected]

2. **Recommendation Success** (1-5):
   - Did the agent provide a clear titration recommendation?
   - Was the recommendation medically appropriate given the patient's data?
   - For contraindications (angioedema, high potassium >5.5, creatinine increase >50%, bronchospasm with beta-blockers), did the agent correctly recommend stopping?
   - For safe titration scenarios, did the agent recommend appropriate dose increases?
   - Score: [1-5]
   - Recommendation given: [Yes/No, and what was it]

3. **Conversation Fluidity** (1-5):
   - How naturally did the conversation flow?
   - Did the agent handle the patient's confusion and contradictions well?
   - Did the agent avoid repetitive or awkward exchanges?
   - Score: [1-5]
   - Issues noted: [list any awkward moments]

4. **Patient Confusion Handling** (1-5):
   - How well did the agent deal with changing answers, out-of-order information, and confusion?
   - Did the agent appropriately seek clarification when needed?
   - Did the agent get stuck or give up when the patient was difficult?
   - Score: [1-5]
   - Examples: [specific instances of good/poor handling]

5. **Safety and Clinical Appropriateness** (1-5):
   - Did the agent correctly identify any contraindications or safety concerns?
   - Was the agent appropriately cautious when uncertain?
   - Did the agent avoid making recommendations when critical information was missing?
   - Score: [1-5]
   - Safety concerns identified: [list any issues]

6. **Overall Effectiveness** (1-5):
   - Overall, did the conversation achieve its goal?
   - Would this interaction be helpful to a real patient?
   - Score: [1-5]

Please provide your evaluation in the following JSON format:
{{
  "information_gathering_completeness": {{
    "score": <1-5>,
    "missing_information": ["item1", "item2"],
    "collected_correctly": ["item1", "item2"]
  }},
  "recommendation_success": {{
    "score": <1-5>,
    "recommendation_provided": <true/false>,
    "recommendation_text": "<what was recommended>",
    "appropriateness": "<assessment of clinical appropriateness>",
    "correct_action": "<what the agent should have recommended>"
  }},
  "conversation_fluidity": {{
    "score": <1-5>,
    "issues": ["issue1", "issue2"],
    "strengths": ["strength1", "strength2"]
  }},
  "confusion_handling": {{
    "score": <1-5>,
    "examples": ["example1", "example2"]
  }},
  "safety_and_clinical": {{
    "score": <1-5>,
    "safety_concerns_identified": ["concern1"],
    "concerns_missed": ["concern1"]
  }},
  "overall_effectiveness": {{
    "score": <1-5>,
    "summary": "<brief summary of performance>"
  }},
  "key_observations": [
    "<observation 1>",
    "<observation 2>"
  ]
}}
"""

def get_patient_response_for_evaluation(client, messages):
    """Get response from Azure OpenAI client for evaluation."""
    try:
        # Azure OpenAI uses chat.completions.create
        response = client.chat.completions.create(
            model="gpt-4.1",  # or whatever model deployment name you're using
            messages=messages,
            temperature=0.3,  # Lower temperature for more consistent evaluation
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting evaluation response: {e}")
        return None

async def evaluate_conversation(conversation_history, patient_data, patient_client):
    """Evaluate a conversation using an LLM judge."""
    evaluator_prompt = get_evaluator_prompt(conversation_history, patient_data)

    # Use Azure OpenAI client
    evaluation_messages = [{"role": "user", "content": evaluator_prompt}]
    evaluation_text = get_patient_response_for_evaluation(patient_client, evaluation_messages)

    if not evaluation_text:
        return {"error": "Failed to get evaluation from LLM"}

    # Extract JSON from the response
    json_match = re.search(r'\{.*\}', evaluation_text, re.DOTALL)
    if json_match:
        try:
            evaluation = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            evaluation = {"error": "Could not parse evaluation", "raw_text": evaluation_text}
    else:
        evaluation = {"error": "Could not find JSON in response", "raw_text": evaluation_text}

    return evaluation

def calculate_aggregate_metrics(all_evaluations):
    """Calculate aggregate statistics across all evaluations."""
    metrics = [
        "information_gathering_completeness",
        "recommendation_success",
        "conversation_fluidity",
        "confusion_handling",
        "safety_and_clinical",
        "overall_effectiveness"
    ]

    aggregate = {}

    for metric in metrics:
        scores = []
        for eval_data in all_evaluations:
            if "error" not in eval_data["evaluation"]:
                if metric in eval_data["evaluation"]:
                    scores.append(eval_data["evaluation"][metric]["score"])

        if scores:
            aggregate[metric] = {
                "mean": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores),
                "count": len(scores)
            }

    return aggregate

# Normal Loop
from typing import Optional

all_evaluations = []
async def run_conversation_loop(
    agent: Any, 
    patient: Dict[str, Any], 
    patient_client: Any,
    quit_commands: Optional[List[str]] = None, 
    debug: bool = False
) -> List[Dict[str, str]]:
    """
    Runs the agent-patient conversation loop.

    Args:
        agent: The initialized Agent instance.
        patient: Dictionary containing patient data.
        patient_client: Client to interact with the simulated patient.
        quit_commands: Commands to stop the loop.
    
    Returns:
        The complete conversation history.
    """
    
    if quit_commands is None:
        quit_commands = ["exit", "goodbye"]

    # Initialize conversation history
    conversation_history = [
        {"role": "system", "content": get_patient_persona(patient)},
        {"role": "user", "content": agent.starting_prompt}
    ]
    print(f"Agent: {agent.starting_prompt}")

    try:
        while True:
            # 1. Patient Response
            patient_response = get_patient_response(patient_client, conversation_history)
            
            # Append patient response to history for the next turn
            conversation_history.append({"role": "assistant", "content": patient_response})
            print(f"Patient: {patient_response}")

            # 2. Check for Quit command
            quit_flag = False
            for quit_command in quit_commands:
                if not patient_response or quit_command in patient_response.lower():
                    quit_flag = True
                    break
            
            if quit_flag:
                break
            
            # 3. Agent Generates Next Turn
            await agent.generate_next_turn(patient_response)
            
            # 4. Get and Log Agent's Response
            agent_prompt = agent.dlg_history[-1].system_response
            conversation_history.append({"role": "user", "content": agent_prompt})
            print(f"Agent: {agent_prompt}")

    except Exception as e:
        print(f"An error occurred during conversation: {e}")
        traceback.print_exc()
        if debug:
            import pdb
            pdb.post_mortem()

    return conversation_history

## 🔁 Main Evaluation Execution
async def run_evaluation_suite(patients: List[Dict[str, Any]], patient_client: Any):
    """
    Runs the full evaluation suite for a list of patients.
    """
    all_evaluations = []

    for patient in patients:
        print("\n" + "="*80)
        print(f"STARTING CONVERSATION WITH {patient['name']}")
        print("="*80)
        
        # 1. Initialize Agent (Needs to be inside the loop for new sessions)
        agent_builder = (
            AgentBuilder(
                name=botname,
                description=description,
                starting_prompt=starting_prompt
            )
            .with_gsheet_specification(gsheet_id_default)
        )
        agent = agent_builder.build(config)

        # 2. Run Conversation Loop
        # The 'with agent:' block was removed and replaced by the correct await call
        conversation_history = await run_conversation_loop(agent, patient, patient_client)

        print("\n" + "="*80)
        print(f"Finished conversation with {patient['name']}")
        print("="*80 + "\n")

        # 3. Evaluate the conversation
        print(f"Evaluating conversation with {patient['name']}...")
        evaluation = await evaluate_conversation(conversation_history, patient, patient_client)
        
        all_evaluations.append({
            "patient_name": patient["name"],
            "patient_data": patient,
            "evaluation": evaluation
        })

        # 4. Print Individual Evaluation
        print("\n" + "="*80)
        print(f"EVALUATION FOR {patient['name']}")
        print("="*80)
        print(json.dumps(evaluation, indent=2))
        print("\n")

    # 5. Aggregate and Print Results
    print("\n" + "="*80)
    print("AGGREGATE RESULTS ACROSS ALL PATIENTS")
    print("="*80 + "\n")
    aggregate_metrics = calculate_aggregate_metrics(all_evaluations)

    for metric, stats in aggregate_metrics.items():
        print(f"\n{metric.replace('_', ' ').title()}:")
        print(f"  Mean Score: {stats['mean']:.2f} / 5.0")
        print(f"  Range: {stats['min']:.1f} - {stats['max']:.1f}")
        print(f"  Sample Size: {stats['count']}")

    # 6. Print Individual Summaries
    print("\n" + "="*80)
    print("INDIVIDUAL PATIENT SUMMARIES")
    print("="*80 + "\n")

    for eval_data in all_evaluations:
        patient_name = eval_data["patient_name"]
        evaluation = eval_data["evaluation"]

        if "error" in evaluation:
            print(f"{patient_name}: EVALUATION ERROR - {evaluation['error']}")
        else:
            overall_score = evaluation.get("overall_effectiveness", {}).get("score", "N/A")
            recommendation = evaluation.get("recommendation_success", {})
            rec_provided = recommendation.get("recommendation_provided", False)
            rec_text = recommendation.get("recommendation_text", "None")

            print(f"{patient_name}:")
            print(f"  Overall Score: {overall_score}/5")
            print(f"  Recommendation Provided: {rec_provided}")
            print(f"  Recommendation: {rec_text}")
            print()

    # 7. Save detailed results to JSON file
    with open('evaluation_results.json', 'w') as f:
        json.dump({
            "individual_evaluations": all_evaluations,
            "aggregate_metrics": aggregate_metrics
        }, f, indent=2)

    print("\nDetailed results saved to 'evaluation_results.json'")

import asyncio
asyncio.run(run_evaluation_suite(patients_array, patient_client))
