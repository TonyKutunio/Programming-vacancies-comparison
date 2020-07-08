from terminaltables import AsciiTable
import headhunter as hh
import superjob as sj


def get_terminaltable(stats, title):
    table_header = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language_name, stats_data in stats.items():
        vacancies_found = stats[language_name]['vacancies found']
        vacancies_processed = stats[language_name]['vacancies processed']
        average_salary = stats[language_name]['expected salary']
        data_table = [language_name, vacancies_found, vacancies_processed, average_salary]
        table_header.append(data_table)
    data_table = AsciiTable(table_header, title)
    return data_table.table


if __name__ == '__main__':

    superjob_title = 'SuperJob Moscow'
    superjob_stats = sj.main()
    superjob_stats_table = get_terminaltable(superjob_stats, superjob_title)
    print(superjob_stats_table)

    headhunter_title = 'HeadHunter Moscow'
    headhunter_stats = hh.main()
    headhunter_stats_table = get_terminaltable(headhunter_stats, headhunter_title)
    print(headhunter_stats_table)
