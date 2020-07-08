import requests
from utils import predict_rub_salary


def get_vacancies(area, search_phrase):
    vacancies = []
    page = 0
    while page < 100:
        url = 'https://api.hh.ru/vacancies'
        headers = {'User-Agent': 'curl'}
        params = {'specialization': 1.221, 'area': area, 'text': search_phrase, 'page': page}
        page_response = requests.get(url, headers=headers, params=params)
        page_response.raise_for_status()
        response_content = page_response.json()

        vacancy = response_content['items']
        vacancies_found = response_content['found']
        vacancies.extend(vacancy)
        page += 1
    return vacancies_found, vacancies


def get_vacancies_with_displayed_salary(vacancies):
    vacancies_with_displayed_salary = []
    for vacancy in vacancies:
        salary = vacancy['salary']
        if salary != None:
            vacancies_with_displayed_salary.append(vacancy)
    return vacancies_with_displayed_salary


def get_vacancies_with_rub_currency(vacancies_with_displayed_salary):
    vacancies_with_rub_currency = []
    for vacancy in vacancies_with_displayed_salary:
        currency = vacancy['salary']['currency']
        if currency == 'RUR':
            vacancies_with_rub_currency.append(vacancy)
    return vacancies_with_rub_currency


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
    area = 1
    search_phrases = [  'Python',
                        'Javascript',
                        'Java',
                        'Ruby',
                        'PHP',
                        'C++',
                        'CSS',
                        'C#',
                        'C',
                        'GO'
    ]

    vacancies_data = {}
    website_name = 'headhunter'
    for search_phrase in search_phrases:
        vacancies_found, vacancies = get_vacancies(area, search_phrase)
        vacancies_with_displayed_salary = get_vacancies_with_displayed_salary(vacancies)
        vacancies_with_rub_currency = get_vacancies_with_rub_currency(vacancies_with_displayed_salary)
        stats = get_vacancy_stats(search_phrase, vacancies_with_rub_currency, vacancies_found, website_name)
        vacancies_data.update(stats)
    return vacancies_data


if __name__ == '__main__':
    main()