import os
import json
import pandas as pd


class PriceMachine():
    
    def __init__(self):
        self.data = []
        self.df_combined = None
        
    def load_prices(self, files_path='/home/mikhail/Downloads/Практическое задание (2)/analysator'):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''

        name_columns = ['название', 'продукт', 'товар', 'наименование']
        price_columns = ['цена', 'розница']
        weight_columns = ['фасовка', 'масса', 'вес']


        for file in os.listdir(files_path):
            if 'price' in file:
                file_path = os.path.join(files_path, file)
                df = pd.read_csv(file_path, sep=',')
               
                name = None
                for col in name_columns:
                    if col in df.columns:
                        name = df.columns[df.columns == col][0]
                        break

                price = None
                for col in price_columns:
                    if col in df.columns:
                        price = df.columns[df.columns == col][0]
                        break

                weight = None
                for col in weight_columns:
                    if col in df.columns:
                        weight = df.columns[df.columns == col][0]
                        break

                if name and price and weight:
                    df_selected = df[[name, weight, price]]
                    df_selected.columns = ['Название', 'Вес', 'Цена']
                    self.data.append(df_selected)
                else:
                    pass

        self.df_combined = pd.concat(self.data, ignore_index=True)
        self.df_combined['Название'] = self.df_combined['Название'].str.lower().str.strip()
        self.df_combined = self.df_combined.sort_values(by='Цена')
        return self.df_combined

    def find_text(self):
        while True:
            request = input("Введите название товара (exit для выхода): ")
            if request.lower() == 'exit':
                break
            else:
                result = self.df_combined[self.df_combined['Название'].str.contains(request.lower())]
                if not result.empty:
                    print("Найденные позиции:")
                    print(result.to_string(index=False))
                else:
                    print("По вашему запросу ничего не найдено")

    def export_to_html(self, fname='/home/mikhail/Downloads/my_output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        self.df_combined.to_html(fname, index=False, encoding='utf-8')
        print(f"HTML: {fname}")

    def _search_product_price_weight(self):
        for index, column in enumerate(self.df_combined.columns):
            print(f"Номер {index+1}: {column}")


    
pm = PriceMachine()
print(pm.load_prices())
pm._search_product_price_weight()
pm.find_text()

print('the end')
pm.export_to_html()
