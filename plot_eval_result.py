import json
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

try:
    with open('evaluation_results.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # with open('evaluation_results_hard.json', 'r', encoding='utf-8') as file:
    #     data_hard = json.load(file)
    # with open('evaluation_results_hardest.json', 'r', encoding='utf-8') as file:
    #     data_hardest = json.load(file)

except Exception as e:
    print(e)

data_for_df = []
for entry in data['individual_evaluations']:
    evaluation = entry['evaluation']
    row = {
        'patient_name': entry['patient_name'],
        'conversation_completed': evaluation['conversation_completed'],
        'information_gathering_completeness': evaluation['information_gathering_completeness']['score'],
        'recommendation_success': evaluation['recommendation_success']['score'],
        'safety_and_clinical': evaluation['safety_and_clinical']['score'],
        'conversation_fluidity': evaluation['conversation_fluidity']['score'],
        'confusion_handling': evaluation['confusion_handling']['score'],
        'overall_effectiveness': evaluation['overall_effectiveness']['score']
    }
    data_for_df.append(row)
print('len1', len(data_for_df))
# for entry in data_hard['individual_evaluations']:
#     evaluation = entry['evaluation']
#     row = {
#         'patient_name': entry['patient_name'],
#         'conversation_completed': evaluation['conversation_completed'],
#         'information_gathering_completeness': evaluation['information_gathering_completeness']['score'],
#         'recommendation_success': evaluation['recommendation_success']['score'],
#         'safety_and_clinical': evaluation['safety_and_clinical']['score'],
#         'conversation_fluidity': evaluation['conversation_fluidity']['score'],
#         'confusion_handling': evaluation['confusion_handling']['score'],
#         'overall_effectiveness': evaluation['overall_effectiveness']['score']
#     }
#     data_for_df.append(row)
# print('len2', len(data_for_df))
# for entry in data_hardest['individual_evaluations']:
#     evaluation = entry['evaluation']
#     row = {
#         'patient_name': entry['patient_name'],
#         'conversation_completed': evaluation['conversation_completed'],
#         'information_gathering_completeness': evaluation['information_gathering_completeness']['score'],
#         'recommendation_success': evaluation['recommendation_success']['score'],
#         'safety_and_clinical': evaluation['safety_and_clinical']['score'],
#         'conversation_fluidity': evaluation['conversation_fluidity']['score'],
#         'confusion_handling': evaluation['confusion_handling']['score'],
#         'overall_effectiveness': evaluation['overall_effectiveness']['score']
#     }
#     data_for_df.append(row)
# print('len3', len(data_for_df))
df = pd.DataFrame(data_for_df)

score_cols = [col for col in df.columns if col not in ['patient_name', 'conversation_completed']]

completed_counts = df['conversation_completed'].value_counts()
completed_counts_df = pd.DataFrame(completed_counts).reset_index()
completed_counts_df.columns = ['Conversation Completed', 'Count']

print("="*50)
print("✅ Finished Conversation")
print("="*50)
print(completed_counts_df)
print("\n")

score_stats = df[score_cols].agg(['mean', 'median', 'std', 'min', 'max', 'count']).T
score_stats = score_stats.round(2)

print("="*50)
print("📊 Stats")
print("="*50)
print(score_stats)
print("\n")

df_long = df.melt(id_vars='patient_name', value_vars=score_cols, var_name='Metric', value_name='Score')
plt.figure(figsize=(12, 7))

plot_data = df_long.groupby(['Metric', 'Score']).size().unstack(fill_value=0)
plot_data.index = plot_data.index.str.replace('_', ' ').str.title()

ax = plot_data.plot(kind='bar', stacked=False, ax=plt.gca(), cmap='viridis')

plt.title('Distribution of Evaluation Scores Across Metrics (Total Entries: 12)', fontsize=16)
plt.xlabel('Evaluation Metric', fontsize=14)
plt.ylabel('Frequency (Count)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(np.arange(0, df_long.shape[0] / len(score_cols) + 1, 1)) # y축을 정수 단위로 설정
plt.legend(title='Score', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plot_filename = 'evaluation_score_distribution.png'
plt.savefig(plot_filename)

