use BikeStore

Go
--Order status: 1 = Pending; 2 = Processing; 3 = Rejected; 4 = Completed

select order_status,
count(order_id)	AS	total_order
from sales.orders


group by order_status
order by order_status

--2

select  C.category_name,
        count (P.product_id) As Product_Count

from production.categories As C

left join   production.products AS P 
            on c.category_id = p.category_id

group by C.category_id,category_name

--3

select      brand_name,
            cast(avg(list_price) AS Decimal(10,2)) As average_price

from      production.products As P

left join   production.brands AS B
            on p.brand_id = b.brand_id
            
group by p.brand_id,b.brand_name

--4

select   brand_name,
max(list_price) AS Most_Expensive_Item
from production.products AS P
left join   production.brands AS B
            on p.brand_id = b.brand_id

group by p.brand_id,brand_name


--5

select first_name,last_name,count(order_id) AS  oprations

from    sales.orders        As  O
left join   sales.staffs    AS  S
            on  S.staff_id = o.staff_id
        

group by S.staff_id,first_name,last_name
order by oprations desc

--6

select first_name,last_name,count(O.order_id) AS Total_Orders
from sales.customers AS C

left join   sales.orders As O
            on c.customer_id    =   o.customer_id  

group by C.customer_id,first_name,last_name

order by Total_Orders desc

--7

select year(order_date) AS  [Year],
count(order_id) AS Total_Orders_PreYear

from sales.orders

group by year(order_date)

--8

select  FORMAT(order_date, 'MMMM')   AS  [MONTH],
        Year(order_date)    AS  [Year],       
        Count(order_id)     AS  Total_orders
from sales.orders
where  Year(order_date) = 2017

group by FORMAT(order_date, 'MMMM') ,Year(order_date)
order By MIN(order_date)

--9

select 
    first_name,last_name,email,count(order_id) As Most_Orders

from 
    sales.orders   AS  O

left join   
        sales.customers AS  C
        on o.customer_id = C.customer_id

group by 
    c.customer_id,first_name,last_name,email

having count(order_id) =(
        select 
            max(order_count)

        from (
                select count(order_id)    AS  order_count
                from sales.orders
                group by customer_id)   AS  customer_max_order)


--10
select 
        store_name,
         count(order_id)  AS  all_orders
from 
        sales.orders  AS  O

left join 
        sales.stores  As  S
                on  s.store_id = o.store_id

group by s.store_id,store_name

