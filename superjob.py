import requests
import os
from dotenv import load_dotenv
from utils import predict_rub_salary


def get_vacancies(catalogue, keyword, town, super_job_secret_key):
    vacancies = []
    page = 0
    while page < 1:
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {'X-Api-App-Id': super_job_secret_key}
        params = {
            'town': town,
            'catalogue': catalogue,
            'keyword': keyword
        }
        page_response = requests.get(url, headers=headers, params=params)
        page_response.raise_for_status()
        response_content = page_response.json()
        vacancy = response_content['objects']
        vacancies_found = response_content['total']
        vacancies.extend(vacancy)
        page += 1

    return vacancies_found, vacancies


def get_vacancies_with_displayed_salary(vacancies):
    vacancies_with_displayed_salary = []
    for vacancy in vacancies:
        payment_from = vacancy['payment_from']
        payment_to = vacancy['payment_to']
        if payment_from != 0 and payment_to != 0:
            vacancies_with_displayed_salary.append(vacancy)
    return vacancies_with_displayed_salary


def get_vacancies_with_rub_currency(vacancies_with_rub_salary):
    rub_vacancies = []
    for vacancy in vacancies_with_rub_salary:
        currency = vacancy['currency']
        if currency == 'rub':
            rub_vacancies.append(vacancy)
    return rub_vacancies


def get_vacancy_stats(language, vacancies_with_rub_currency, vacancies_found, website_name):
    average_salaries_sum = 0
    vacancies_comparison = {}
    language_kind = []
    for vacancy_number, vacancy in enumerate(vacancies_with_rub_currency):
        average_salary = predict_rub_salary(vacancy, website_name)
        average_salaries_sum += average_salary
        expected_average_salary = int(average_salaries_sum / (vacancy_number + 1))

        vacancies_comparison['vacancies found'] = vacancies_found
        vacancies_comparison['vacancies processed'] = vacancy_number + 1
        vacancies_comparison['expected salary'] = expected_average_salary
        language_kind = {language: vacancies_comparison}
    return language_kind


def main():
    load_dotenv()
    super_job_secret_key = os.getenv('SUPER_JOB_SECRET_KEY')
    town = 'Москва'
    catalogue = 'Разработка, программирование'
    keywords = [
        'Python', 'Javascript',
        'Java', 'Ruby',
        'PHP', 'C++',
        'CSS', 'C#',
        'C', 'GO'
    ]
    vacancies_data = {}
    website_name = 'superjob'
    for keyword in keywords:
        vacancies_found, vacancies = get_vacancies(catalogue, keyword, town, super_job_secret_key)
        vacancies_with_displayed_salary = get_vacancies_with_displayed_salary(vacancies)
        vacancies_with_rub_currency = get_vacancies_with_rub_currency(vacancies_with_displayed_salary)
        stats = get_vacancy_stats(keyword, vacancies_with_rub_currency, vacancies_found, website_name)
        vacancies_data.update(stats)
    return vacancies_data


if __name__ == '__main__':
    main()