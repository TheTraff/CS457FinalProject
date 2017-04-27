"""
Final Project for CS457 - implement a basic DBMS
Ben Traffanstedt
Spring 2017
"""
import os
import sys
from pprint import pprint

db_path = 'dbs/'
class QueryExecutor(object):
    """
    the main class that manages parsing the Query
    and reading the items from the multiple dbs
    """

    def __init__(self, query, security_level):
        """
        parses the query, and divides it up into the 
        select, from and where conditions
        @input
        query(string): the string representation of the query
        security_level(int): the specified security level of the user
        """

        query_parts = query.split(' ')
        self.security_level = security_level

        self.select_conds = []
        self.from_conds = []        
        self.where_conds = []

        #flags to keep track of which part of the query we are on 
        select_flag = False
        from_flag = False
        where_flag = False
        for option in query_parts:
            #remove commas and semicolons
            option = option.translate(None, ',;')

            #run through the options in the query
            if option == 'SELECT':
                from_flag = False
                where_flag = False
                select_flag = True
            if option == 'FROM':
                select_flag = False
                where_flag = False
                from_flag = True
            if option == 'WHERE':
                from_flag = False
                select_flag = False
                where_flag = True
            
            if select_flag and option != 'SELECT':
                self.select_conds.append(option)
            if from_flag and option != 'FROM':
                self.from_conds.append(option)
            if where_flag and option != 'WHERE':
                self.where_conds.append(option)
            
        print(self.select_conds)
        print(self.from_conds)
        print(self.where_conds)

    def run_query(self):
        """
        the main process responsible for running the query
        on the databases
        """
        from_opts = self.from_conds
        select_opts = self.select_conds
        where_opts = self.where_conds

        #execute the from portion of the query
        #and load those files for reading
        #dbs = {filename: open(db_path + filename, 'r') for filename in from_opts}
        dbs = {}
        for db_name in from_opts:
            dbs[db_name] = open(db_path + db_name, 'r')


        db_columns = {}
        for item in dbs:
            columns = dbs[item].readline().split('\t')
            columns[-1] = columns[-1].rstrip()
            db_columns[item] = columns
        
        print(db_columns)
        
        where_operations = {}
        for option in where_opts:
            #seperate the left and right sides of the operation
            if option != 'AND':     
                operands = option.split('=')
                try:
                    where_operations[operands[0]].append(operands[1])
                except KeyError:
                    #if we haven't run into this left operand before, make the spot a list
                    where_operations[operands[0]] = []
                    where_operations[operands[0]].append(operands[1])
        
        print(where_operations)

        column_nums = {}
        for column in db_columns:
            column_nums[column] = []
            #append the PK security label column
            column_nums[column].append(1)

            for left_op in where_operations:
                if left_op in db_columns[column]:
                    #the column number is the index of the column name in the db_columns dict
                    column_nums[column].append(db_columns[column].index(left_op))

            #append the tuple security label column
            column_nums[column].append(-1)
        
        #select all the tuples that meet the basic where options, i.e. A=3, B=65, etc.
        print(column_nums)
        table_tuples = {}
        for table in dbs:
            table_tuples[table] = []
            for row in dbs[table]:
                row_items = row.split('\t')
                row_items[-1] = row_items[-1].rstrip()
                #check the security labels first
                compare_columns = column_nums[table]
                #the two labels are always the first and last items in the compare_columns
                KC_label = compare_columns[0]
                TC_label = compare_columns[-1]
                if int(row_items[KC_label]) <= self.security_level and int(row_items[TC_label]) <= self.security_level:
                    for column in compare_columns[1:-1]:
                        
                        if row_items[column] == 
                    table_tuples[table].append(row_items)
        
        pprint(table_tuples)
        cartesian_tuples = []
        
        #for first_tables_tuples in table_tuples[from_opts[0]]: #need to use from_opts here to keep it in order

         




def main():
    security_level = -1
    while security_level > 4 or security_level <= 0:
        security_level = input('enter your security level:')
        if security_level > 4 or security_level < 0:
            print('please enter a valid security level')
    

    queries = raw_input('input your query: ')
    queries_list = queries.split(';')
    #pop the last element to get rid of the possilbe blank space after the 
    queries_list.pop()
    print(queries_list)
    for query in queries_list:
        executor = QueryExecutor(query.upper(), security_level)
        executor.run_query()


if __name__=='__main__':
    main()
