
def get_salary_range(rub_vacancy, website_name):
    if website_name == 'headhunter':
        salary_from = rub_vacancy['salary']['from']
        salary_to = rub_vacancy['salary']['to']
    else:
        salary_from = rub_vacancy['payment_from']
        salary_to = rub_vacancy['payment_to']
    return salary_from, salary_to


def predict_rub_salary(salary_from, salary_to):
    average_salary = 0
    if salary_from == None or salary_to == 0:
        salary_from = salary_to * 0.8
    elif salary_to == None or salary_to == 0:
        salary_to = salary_from * 1.2
    average_salary += (salary_from + salary_to) / 2
    return int(average_salary)
