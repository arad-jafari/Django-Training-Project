from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

QUERIES = {
    1: """
SELECT 
    CASE order_status
        WHEN 1 THEN 'Pending'
        WHEN 2 THEN 'Processing'
        WHEN 3 THEN 'Rejected'
        WHEN 4 THEN 'Completed'
    END AS order_status_text,
    COUNT(order_id) AS total_order
FROM sales.orders
GROUP BY order_status
ORDER BY order_status;
    """,
    2: """
        SELECT C.category_name, COUNT(P.product_id) AS Product_Count
        FROM production.categories AS C
        LEFT JOIN production.products AS P ON C.category_id = P.category_id
        GROUP BY C.category_id, C.category_name
    """,
    3: """
        SELECT brand_name, CAST(AVG(list_price) AS Decimal(10,2)) AS average_price
        FROM production.products AS P
        LEFT JOIN production.brands AS B ON P.brand_id = B.brand_id
        GROUP BY P.brand_id, B.brand_name
    """,
    4: """
        SELECT brand_name, MAX(list_price) AS Most_Expensive_Item
        FROM production.products AS P
        LEFT JOIN production.brands AS B ON P.brand_id = B.brand_id
        GROUP BY P.brand_id, B.brand_name
    """,
    5: """
SELECT first_name, last_name, COUNT(order_id) AS oprations
FROM sales.orders AS O
LEFT JOIN sales.staffs AS S
    ON S.staff_id = O.staff_id
GROUP BY S.staff_id, first_name, last_name
HAVING COUNT(order_id) > 0
ORDER BY oprations DESC;
    """,
    6: """

        SELECT top 100 first_name, last_name,email, COUNT(O.order_id) AS Top100_Customer_Total_Orders
        FROM sales.customers AS C
        LEFT JOIN sales.orders AS O ON C.customer_id = O.customer_id
        GROUP BY C.customer_id, first_name, last_name,email
        ORDER BY Top100_Customer_Total_Orders DESC
    """,
    7: """
        SELECT YEAR(order_date) AS [Year], COUNT(order_id) AS Total_Orders_PreYear
        FROM sales.orders
        GROUP BY YEAR(order_date)
    """,
    8: """
        SELECT FORMAT(order_date, 'MMMM') AS [MONTH], YEAR(order_date) AS [Year], COUNT(order_id) AS Total_orders_PreMonth_2017
        FROM sales.orders
        WHERE YEAR(order_date) = 2017
        GROUP BY FORMAT(order_date, 'MMMM'), YEAR(order_date)
        ORDER BY MIN(order_date)
    """,
    9: """
        SELECT first_name, last_name, email, COUNT(order_id) AS Most_Orders
        FROM sales.orders AS O
        LEFT JOIN sales.customers AS C ON O.customer_id = C.customer_id
        GROUP BY C.customer_id, first_name, last_name, email
        HAVING COUNT(order_id) = (
            SELECT MAX(order_count)
            FROM (
                SELECT COUNT(order_id) AS order_count
                FROM sales.orders
                GROUP BY customer_id
            ) AS customer_max_order
        )
    """,
    10: """
        SELECT store_name, COUNT(order_id) AS all_orders
        FROM sales.orders AS O
        LEFT JOIN sales.stores AS S ON S.store_id = O.store_id
        GROUP BY S.store_id, store_name"""
}

def dashboard(request):
    queries = [
        (1, "Total Orders by Status"),
        (2, "Products per Category"),
        (3, "Average Price per Brand"),
        (4, "Most Expensive Item per Brand"),
        (5, "Orders by Staff"),
        (6, "Orders by Customer"),
        (7, "Total Orders per Year"),
        (8, "Orders by Month in 2017"),
        (9, "Customer with Most Orders"),
        (10, "Orders by Store"),
    ]
    return render(request, 'dashboard.html', {'queries': queries})


QUERY_TEXTS = [
    "Total Orders by Status",
    "Product Count per Category",
    "Average Product Price per Brand",
    "Most Expensive Item per Brand",
    "Operations by Staff",
    "Total Orders per Customer",
    "Orders per Year",
    "Monthly Orders for 2017",
    "Customer with Most Orders",
    "Total Orders per Store"
]

def query_view(request, query_id):
    sql = QUERIES[query_id]
    with connection.cursor() as cursor:
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]##?
        rows = cursor.fetchall()

        table_data = [dict(zip(columns, row)) for row in rows]

    # Get the query name for header
    try:
        query_name = QUERY_TEXTS[query_id - 1]
    except IndexError:
        query_name = f"Query {query_id}"

    return render(request, 'query.html', {
        'columns': columns,
        'data': table_data,
        'query_name': query_name,
    })

