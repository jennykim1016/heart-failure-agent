# heart-failure-agent
cs224v project

To set up:
(1) clone the genie-worksheets directory and install the necessary env by following [here](https://github.com/stanford-oval/genie-worksheets?tab=readme-ov-file#installation). Please make sure none of your conda / virtual environments are activated when proceeding with these lines.

```
git clone https://github.com/stanford-oval/genie-worksheets.git
cd worksheets
uv venv
source venv/bin/activate
uv sync
```

(2) Place all these python files to the main folder.

(3) For `env_setting.py`, move it to the main folder and fill in the credential details for OpenAI (we have pre-filled our credential in the submission, but you may need to use yours)

(4) For code execution: run `python heart_failure_agent.py`. Here, you can choose the patient persona among the bottom three.

```
await run_and_evaluate_conversation(patients, get_patient_persona)
await run_and_evaluate_conversation(patients, get_patient_persona_hard)
await run_and_evaluate_conversation(patients, get_patient_persona_hardest)
```

(5) For plotting, run `python plot_eval_result.py`.
