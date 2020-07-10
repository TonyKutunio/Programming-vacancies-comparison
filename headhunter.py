import requests
from utils import get_salary_range
from utils import predict_rub_salary


def get_vacancies(area, search_phrase):
    vacancies = []
    page = 0
    while page < 100:
        url = 'https://api.hh.ru/vacancies'
        headers = {'User-Agent': 'curl'}
        params = {'specialization': 1.221,
                  'area': area,
                  'text': search_phrase,
                  'page': page
        }
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


def get_rub_vacancies(vacancies_with_displayed_salary):
    rub_vacancies = []
    for vacancy in vacancies_with_displayed_salary:
        currency = vacancy['salary']['currency']
        if currency == 'RUR':
            rub_vacancies.append(vacancy)
    return rub_vacancies


def get_vacancy_stats(language, rub_vacancy,
                      vacancies_found, website_name):
    average_salaries_sum = 0
    vacancies_comparison = {}
    language_kind = []
    for vacancy_number, vacancy in enumerate(rub_vacancy):
        salary_from, salary_to = get_salary_range(vacancy, website_name)



        average_salary = predict_rub_salary(salary_from, salary_to)
        average_salaries_sum += average_salary
        expected_average_salary = average_salaries_sum / (vacancy_number + 1)

        vacancies_comparison['vacancies found'] = vacancies_found
        vacancies_comparison['vacancies processed'] = vacancy_number + 1
        vacancies_comparison['expected salary'] = int(expected_average_salary)
        language_kind = {language: vacancies_comparison}
    return language_kind

def main():
    area = 1
    keywords = [
        'Python', 'Javascript',
        'Java', 'Ruby',
        'PHP', 'C++',
        'CSS', 'C#',
        'C', 'GO'
    ]

    vacancies_data = {}
    website_name = 'headhunter'
    for keyword in keywords:
        vacancies_found, vacancies = get_vacancies(area, keyword)
        vacancies_with_displayed_salary = get_vacancies_with_displayed_salary(
                                                                    vacancies)
        rub_vacancy = get_rub_vacancies(vacancies_with_displayed_salary)
        stats = get_vacancy_stats(keyword, rub_vacancy,
                                  vacancies_found, website_name)
        vacancies_data.update(stats)
    return vacancies_data


if __name__ == '__main__':
    main()
