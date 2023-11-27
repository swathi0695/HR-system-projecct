import pandas as pd

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .settings import PAGINATION

from sqlalchemy import text
from pyspark.sql.functions import col, to_date

from .common_module import query_from_db, pyspark_utils


@api_view(['GET'])
def read_all_employees(request:object) -> object:
    """
    This function retrieves all employee records from the database.
    Args:
    param1 (type): request object.
    
    Returns:
    list[dict, ..., dict]: returns list of dictionaries with each dictionaries having each employee deatils.
    """
    try:
        engine = query_from_db.create_connection()
        print(engine)
        df = query_from_db.read_data_from_db(engine)

        # Sort employees (default sort by ID)
        sort_by = request.GET.get('sort_by', 'id')
        if sort_by in df.columns:
            data = df.sort_values(by=sort_by)

        # Filtering
        filter_params = {}
        # Add your filtering logic based on request parameters (e.g., industry, salary range, etc.)
        industry = request.GET.get('industry')
        if industry:
            filter_params['industry'] = industry
            # Apply filters
            for key, value in filter_params.items():
                data = data[data[key] == value]

        # Convert filtered and paginated data to JSON
        data = data.to_dict(orient='records')

        # Pagination setup
        if 'page_size' in request.query_params:
            if request.GET['page_size'] is not None:
                paginator = PageNumberPagination()
                paginator.page_size = int(request.GET.get('page_size', PAGINATION['PAGE_SIZE']))
                data = paginator.paginate_queryset(data, request)
        return Response(data)

    except Exception as e:
        print(f"Error in read_all_employees method : {e}")
        raise e


@api_view(['GET'])
def read_one_record(request: object, employee_id: int) -> object:
    """
    This function retrieves one employee record from the database matching the employee_id
    Args:
    param1 (object): request
    param2 (int): employee_id
    
    Returns:
    list[dict]: returns list of dictionary with employee deatils with macthing employee_id.
    """
    try:
        if not isinstance(employee_id, int):
            return {"message" : f"{employee_id} is not valid interger"}

        engine = query_from_db.create_connection()
        query = f"select * from employees where id = {employee_id}"
        df = pd.read_sql(query, engine)
        df = df.to_dict(orient="records")
        return Response(df)
    except Exception as e:
        print(f"Error in read_one_record method : {e}")
        raise e


@api_view(['PUT'])
def update_employee(request: object) -> object:
    """
    This function updates an employee record based on the request body.
    Args:
    param1 (object): request
    
    Returns:
    dict: returns success message once updated in the database 
    """
    try:
        input_req = {}
        for req_data in request.data.items():
            input_req[req_data[0]] = req_data[1]
        if 'id' not in input_req:
            return Response({"message" : "id is required field in for /employee/update api"})
        
        set_clause = ""
        where_clause = f" WHERE id = {input_req['id']}"

        for key, value in input_req.items():
            if value == "" or key == 'id' or value is None:
                continue
            elif isinstance(value, str):
                set_clause += f"{key} = \'{value}\', "
            else:
                set_clause += f"{key} = {value}, "

        update_query = "UPDATE employees SET " + set_clause[:-2] + where_clause

        engine = query_from_db.create_connection()
        with engine.connect() as connection:
            connection.execute(text(update_query))
            connection.commit()
        return Response({"message": "udpate success"})
    except Exception as e:
        print(f"Error in update_employee method : {e}")
        raise e



@api_view(['DELETE'])
def delete_employee(request: object, employee_id: int):
    """
    This function deletes an employee record from the database matching the employee_id
    Args:
    param1 (object): request
    param2 (int): employee_id
    
    Returns:
    dict: returns success message once deleted from the database 
    """
    try:
        delete_query = f"DELETE FROM employees WHERE id = {employee_id}"
        print("delete_query --->\n", delete_query)
        engine = query_from_db.create_connection()
        with engine.connect() as connection:
            print(connection.execute(text(delete_query)))
            connection.commit()
            return Response({"message": "delete sucess"})
    except Exception as e:
        connection.rollback()
        print(f"Error while deleting record : {e}")
        raise e
    finally:
        connection.close()


@api_view(['POST'])
def insert_record_into_table(request: object) -> object:
    insert_query = f"INSERT INTO employees (id, first_name, last_name,email,gender,date_of_birth,industry,salary,years_of_experience) VALUES (1,'Annmarie','Crooke','acrooke0@gizmodo.com','M','09/07/1978','Other Specialty Stores',180466.37,10)"
    engine = query_from_db.create_connection()
    with engine.connect() as connection:
        print(connection.execute(text(insert_query)))
        connection.commit()
    return Response({"message": "insert success"})


@api_view(['GET'])
def get_average_age_per_industry(request: object) -> object:
    """
    Calculate the average age per industry.
    Args:
    param1 (object): request
    
    Returns:
    dict: A dictionary where keys represent industries and values represent the average age of employees in that industry.
    """
    try:
        df, spark_session_obj = pyspark_utils.read_table_data_using_spark()

        # Convert date_of_birth to a date format and calculate age
        df = df.withColumn("date_of_birth", to_date(col("date_of_birth"), "dd/MM/yyyy")) \
                .withColumn("age", pyspark_utils.calculate_age(col("date_of_birth")))

        # Calculate average age per industry
        avg_age_per_industry = df.groupBy("industry").agg({"age": "avg"}).collect()
        res = {}
        # print("type of avg_age_per_industry --->",type(avg_age_per_industry))
        for i in range(len(avg_age_per_industry)):
            res[avg_age_per_industry[i][0]] = avg_age_per_industry[i][1]
        return Response(res)
    except Exception as e:
        print(f"Error while get_average_age_per_industry record : {e}")
        raise e
    finally:
        spark_session_obj.stop()


@api_view(['GET'])
def get_average_salary_per_industry(request: object) -> object:
    """
    Calculate the average salary per industry.
    Args:
    param1 (object): request
    
    Returns:
    dict: A dictionary where keys represent industries and values represent the average salary of employees in that industry.
    """
    try:
        res = {}
        df, spark_session_obj = pyspark_utils.read_table_data_using_spark()

        # Calculate average salaries per industry
        avg_salary_per_industry = df.groupBy("industry").agg({"salary": "avg"}).collect()
        for i in range(len(avg_salary_per_industry)):
            res[avg_salary_per_industry[i][0]] = avg_salary_per_industry[i][1]
        return Response(res)
    except Exception as e:
        print(f"Error while get_average_salary_per_industry record : {e}")
        raise e
    finally:
        spark_session_obj.stop()


@api_view(['GET'])
def get_average_salary_per_years_of_exp(request: object) -> object:
    """
    Calculate the average salary per years of experience.
    Args:
    param1 (object): request
    
    Returns:
    dict: A dictionary where keys represent years of experience and values represent the average salary of employees with that experience.
    {
            "average_salary_per_years_of_exp": [
                {
                    "years_of_experience": float,
                    "avg_salary": float
                },
                # More entries for different years_of_experience
            ]
        }
    """
    try:
        final_res = []
        df, spark_session_obj = pyspark_utils.read_table_data_using_spark()

        # Calculate average salaries per years of experience
        avg_salary_per_experience = df.groupBy("years_of_experience").\
                                    agg({"salary": "avg"}).collect()
        for i in range(len(avg_salary_per_experience)):
            result_data = {
                "years_of_experience" : avg_salary_per_experience[i][0],
                "avg_salary" : avg_salary_per_experience[i][1]
            }
            final_res.append(result_data)
        return Response({"average_salary_per_years_of_exp" : final_res})
    except Exception as e:
        print(f"Error while get_average_salary_per_years_of_exp record : {e}")
        raise e
    finally:
        spark_session_obj.stop()


@api_view(['GET'])
def get_other_interesting_stats(request: object) -> object:
    """
    Calculates some other interesting statistics from the data like, 
    gender count in the data, average salary of by gender, top industries with highest employee count.
    Args:
    param1 (object): request
    
    Returns:
    dict: dictionary of dictionaries having details of the statistics.
    {
        "gender_count": dict,
        "avg_salary_by_gender" : dict,
        "top_industries" : dict
    }
    """
    try:
        df, spark_session_obj = pyspark_utils.read_table_data_using_spark()
        gender_count = df.groupBy("gender").count().collect()
        avg_salary_by_gender = df.groupBy("gender").\
                                agg({"salary": "avg"}).collect()
        top_industries = df.groupBy("industry").count().\
                                orderBy(col("count").desc()).limit(10).collect()
        
        gender_count_dict = {}
        for i in range(len(gender_count)):
            gender_count_dict[gender_count[i][0]] = gender_count[i][1]
        
        avg_salary_by_gender_dict = {}
        for i in range(len(avg_salary_by_gender)):
            avg_salary_by_gender_dict[avg_salary_by_gender[i][0]] = avg_salary_by_gender[i][1]
        
        top_industries_dict = {}
        for i in range(len(top_industries)):
            top_industries_dict[top_industries[i][0]] = top_industries[i][1]

        res = {
            "gender_count" : gender_count_dict,
            "avg_salary_by_gender" : avg_salary_by_gender_dict,
            "top_industries" : top_industries_dict
        }
        return Response(res)
    except Exception as e:
        print(f"Error while get_other_interesting_stats record : {e}")
        raise e
    finally:
        spark_session_obj.stop()
