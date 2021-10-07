def stockAndSales(daxWeek):
    return """
            EVALUATE
            SELECTCOLUMNS(
                FILTER(
                    SUMMARIZECOLUMNS(
                        'Product Hierarchy PRH'[PRH Department ID],
                        'Product Hierarchy PRH'[PRH Category ID],
                        'Planning Calendar PCAL'[PCAL_MONTH_KEY],
                        'Planning Calendar PCAL'[PCAL_WEEK_KEY],
                        'Stores STR'[STR Number],
                        FILTER(
                            VALUES('Planning Calendar PCAL'[PCAL_WEEK_KEY]),
                            'Planning Calendar PCAL'[PCAL_WEEK_KEY] = """ + str(daxWeek) + """
                        ),
                        FILTER (
                            VALUES ( 'Product Hierarchy PRH'[PRH Division] ),
                            ( 'Product Hierarchy PRH'[PRH Division] IN { "a Clothing", "b Nonclothing" } )
                        ),
                        "SalesValue",
                        [Sales Retail Report dsale],
                        "SalesQty",
                        [Sales Qty dsale],
                        "StockQty",
                        [Closing Stock on Hand Qty dcssd],
                        "MonthNew",
                        "Y"&LEFT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_MONTH_KEY]), STRING),4)&"M"&RIGHT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_MONTH_KEY]), STRING),2),
                        "WeekNew",
                        "Y"&LEFT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_WEEK_KEY]), STRING),4)&"W"&RIGHT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_WEEK_KEY]), STRING),2)
                        ),
                        OR([SalesValue] > 0,
                        [StockQty] > 0)
                        ),
                "PRHDepartmentID",
                [PRH Department ID],
                "PRHCategoryID",
                [PRH Category ID],
                "STRNumber",
                'Stores STR'[STR Number],
                "MonthNew",
                [MonthNew],
                "WeekNew",
                [WeekNew],
                "SalesValue",
                [SalesValue],
                "SalesQty",
                [SalesQty],
                "StockQty",
                [StockQty]
                )
    """


def sales(daxWeek):
    return """
            EVALUATE
            SELECTCOLUMNS(
            FILTER(
            SUMMARIZECOLUMNS(
            'Product Hierarchy PRH'[PRH Category ID],
            'Planning Calendar PCAL'[PCAL_MONTH_KEY],
            'Planning Calendar PCAL'[PCAL_WEEK_KEY],
            'Stores STR'[STR Number],
            FILTER(
            VALUES('Planning Calendar PCAL'[PCAL_WEEK_KEY]),
            'Planning Calendar PCAL'[PCAL_WEEK_KEY] = """ + str(daxWeek) + """
            ),
            FILTER(
            VALUES('Product Hierarchy PRH'[PRH PEPCO]),
            'Product Hierarchy PRH'[PRH PEPCO] IN {"a Merchandise"}
            ),
            "SalesValue",
            [Sales Retail Report dsale],
            "SalesQty",
            [Sales Qty dsale],
            "MonthNew",
            "Y"&LEFT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_MONTH_KEY]), STRING),4)&"M"&RIGHT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_MONTH_KEY]), STRING),2),
            "WeekNew",
            "Y"&LEFT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_WEEK_KEY]), STRING),4)&"W"&RIGHT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_WEEK_KEY]), STRING),2)
            ),
            [SalesValue] > 0
            ),
            "PRHCategoryID",
            [PRH Category ID],
            "STRNumber",
            'Stores STR'[STR Number],
            "MonthNew",
            [MonthNew],
            "WeekNew",
            [WeekNew],
            "SalesValue",
            [SalesValue],
            "SalesQty",
            [SalesQty]
            )
    """


def stock(daxWeek):
    return """
        EVALUATE         
        SELECTCOLUMNS(
        FILTER(
        SUMMARIZECOLUMNS(
        'Product Hierarchy PRH'[PRH Category ID],
        'Planning Calendar PCAL'[PCAL_MONTH_KEY],
        'Planning Calendar PCAL'[PCAL_WEEK_KEY],
        'Stores STR'[STR Number],
        FILTER(
        VALUES('Planning Calendar PCAL'[PCAL_WEEK_KEY]),
        'Planning Calendar PCAL'[PCAL_WEEK_KEY] = """ + str(daxWeek) + """
        ),
        FILTER(
        VALUES('Product Hierarchy PRH'[PRH PEPCO]),
        'Product Hierarchy PRH'[PRH PEPCO] IN {"a Merchandise"}
        ),
        "StockQty",
        [Closing Stock on Hand Qty dcssd],
        "MonthNew",
        "Y"&LEFT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_MONTH_KEY]), STRING),4)&"M"&RIGHT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_MONTH_KEY]), STRING),2),
        "WeekNew",
        "Y"&LEFT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_WEEK_KEY]), STRING),4)&"W"&RIGHT(CONVERT(MAX('Planning Calendar PCAL'[PCAL_WEEK_KEY]), STRING),2)
        ),
        [Closing Stock on Hand Qty dcssd] > 0
        ),
        "PRHCategoryID",
        [PRH Category ID],
        "STRNumber",
        'Stores STR'[STR Number],
        "MonthNew",
        [MonthNew],
        "WeekNew",
        [WeekNew],
        "StockQty",
        [Closing Stock on Hand Qty dcssd]
        )        
    """


def weeks(startEndWeeks):
    daxStartWeek = startEndWeeks[0][1:5] + startEndWeeks[0][6:8]
    daxEndWeek = startEndWeeks[1][1:5] + startEndWeeks[1][6:8]

    return """
            EVALUATE
            SUMMARIZECOLUMNS (
                'Planning Calendar PCAL'[PCAL_WEEK_KEY],
                FILTER (
                    VALUES ( 'Planning Calendar PCAL'[PCAL_WEEK_KEY] ),
                    'Planning Calendar PCAL'[PCAL_WEEK_KEY] >= """ + str(daxStartWeek) + """
                        && 'Planning Calendar PCAL'[PCAL_WEEK_KEY] <= """ + str(daxEndWeek) + """
                )
            )
    """
