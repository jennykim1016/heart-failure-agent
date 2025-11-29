# heart-failure-agent
cs224v project

To set up:
(1) clone the genie-worksheets directory [here](https://github.com/stanford-oval/genie-worksheets?tab=readme-ov-file#installation)
(2) install the necessary env by following [here](https://github.com/stanford-oval/genie-worksheets?tab=readme-ov-file#installation)
(3) create the file env_setting.py in the main folder by filling in the details

env_content = """
LLM_API_KEY="TODO"
LLM_API_ENDPOINT="TODO"
LLM_API_VERSION="TODO"
"""

env_content_dict = {'LLM_API_KEY': 'TODO',
               'LLM_API_ENDPOINT': 'TODO',
               'LLM_API_VERSION': 'TODO'}

and (4) place the heart_failure_agent.py file into the same home directory and run the file by running `python heart_failure_agent.py`.

For plotting, run (5) plot_eval_result.py
