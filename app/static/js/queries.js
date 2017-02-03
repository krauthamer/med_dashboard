var smokingQuery = 'select user_id, problem_names, medication_names, allergy_names, procedure_names, immunization_names from combo where ( problem_names like "' + '%' + 'smok' +'%" or problem_names like "%bupropion%" or problem_names like "%nicotine dep%" or problem_names like "' + '%' + 'cigarette%" or problem_names like "%tobacco%") and problem_names not like "' + '%' +'former smok%" group by user_id;';

var prediabetesQuery = 'select user_id, problem_names, medication_names, allergy_names, procedure_names, immunization_names from combo where problem_names like "%prediabet%" and problem_names not like "%diabetes type%" and problem_names not like "%diabetes m%" group by user_id order by user_id;';

var diabetesQuery = 'select user_id, problem_names, medication_names, allergy_names, procedure_names, immunization_names from combo where  problem_names not like "%prediabet%" and problem_names like "%diabet%" group by user_id order by user_id;';

var adhdQuery = 'select user_id, problem_names, medication_names, allergy_names, procedure_names, immunization_names from combo where problem_names like "%ADHD%" or problem_names like "%attention def%" or medication_names like "%adderall%" group by user_id order by user_id;';

var osaQuery = 'select user_id, problem_names, medication_names, allergy_names, procedure_names, immunization_names from combo where  problem_names like "%osa%" or problem_names like "%apnea%" group by user_id order by user_id;';

var anxietyQuery = 'select user_id, problem_names, medication_names, allergy_names, procedure_names, immunization_names from combo where  problem_names like "%panic d%" or problem_names like "%anxi%" group by user_id order by user_id;';

var depressionQuery = 'select user_id, problem_names, medication_names, allergy_names, procedure_names, immunization_names from combo where  problem_names like "%depress%" group by user_id order by user_id;';

var highriskpregnancyQuery = 'select user_id, problem_names, medication_names, allergy_names, procedure_names, immunization_names from combo where  problem_names like "%high_risk preg%" group by user_id order by user_id;';
