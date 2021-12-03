import functions as f
import daxDownloader as dd
import daxQueries as dq

import pandas as pd
import os
import tqdm


choices_list = [0, 1, 2, 3]
choices = """
            Wybierz akcję:
            0. Lista tygodni w istniejącym pliku.
            1. Pobierz plik na nowo.
            2. Dociągnij tygodnie do istniejącego pliku (zanim to wybierzez sprawdź jakie tygodnie są już pobrane).
            3. Zrezygnuj."""


def stockAndSales_toCSV(filePath, weeks):
    #tqdmLoop = tqdm.tqdm(weeks[0])
    #weeks = list(weeks)
    weeks_list = weeks.split()

    for week in weeks_list:
        #tqdmLoop.set_description("Pobierany tydzień %s" % week)
        w = week.split(',')[0]
        print(f"Week: {w}")
        try:
            stockAndSales = dd.dataFrameFromTabular(dq.stockAndSales(w))
            stockAndSales.fillna(0, inplace=True)
            stockAndSales.to_csv(filePath, header=False, index=False, mode="a+")
        except:
            errorMessage = """
                        ### [ERROR] ###
                        Coś poszło nie tak!
                        aktualnie pobierany tydzień nie został pobrany.
                        Spróbuj uruchomić program ponownie.
                        Pamiętaj, że nie musisz pobierać wszystkich tygodni od początku.
                        Pogram Cię poinstruuje jak dociągnąć brakujące tygodnie.
                        ### [ERROR] ###
                        """
            print(errorMessage)

            return


def run(filePath):
    print(choices)
    choice = input()

    if choice == str(0):
        try:
            stockAndSales = pd.read_csv(filePath)
            print("Lista tygodni, które znajudują się w pliku: ", stockAndSales.Week.unique())
        except:
            print("Prawdopodobnie nie ma pliku ze stockiem i sprzedażą w podanym folderze.")

        run(filePath)

    if choice == str(1):
        print("Ustaw początkowy i końcowy tydzień, dla którego ma być wyliczony lost sales.")
        startEndWeeks = f.setStartEndWeeks()

        weeks = dd.dataFrameFromTabular(dq.weeks(startEndWeeks))

        if os.path.isfile(filePath):
            os.remove(filePath)

        stockAndSales = pd.DataFrame(columns=["DepartmentID", "CategoryID", "StrNumber", "Month", "Week", "SalesValue",
                                              "SalesQty", "StockQty"])
        stockAndSales.to_csv(filePath, index=False)

        stockAndSales_toCSV(filePath, weeks)

    if choice == str(2):
        print("Ustaw początkowy i końcowy tydzień, dla którego mają zostać dociągnięte dane.")
        startEndWeeks = f.setStartEndWeeks()

        weeks = dd.dataFrameFromTabular(dq.weeks(startEndWeeks))

        if not os.path.isfile(filePath):
            print("Nie ma pliku w skazanym folderze.")
            run(filePath)

        stockAndSales_toCSV(filePath, weeks)


# run(r"C:\All\Python Projects\testy\StockAndSales.csv")
