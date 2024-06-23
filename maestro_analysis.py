# -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
# # plt.plot([2, 4, 6, 8, 10, 12, 14], [2, 5, 7, 8, 8, 8,0])
# plt.show()
import dateutil
from numpy.core.fromnumeric import var
import pymonetdb
from datetime import datetime, date, time
from dateutil.parser import parse
import json
import pandas as pd
import os, sys
import string
import numpy as np
from matplotlib.pylab import plt
import matplotlib.pyplot
import pylab
import statistics
from dateutil import parser
from psutil._common import bytes2human

from functions.AbstractWf import isValid

connection = pymonetdb.connect(username="monetdb", password="monetdb", hostname="localhost", database="voc")


# removepipe = connection.cursor()
# removepipe.arraysize = 1000
# removepipe.execute('select execution_datetime from data_transformation_execution where data_transformation_id = 4 limit 7')
# list = removepipe.fetchall()

# select_times = connection.cursor()
# select_times.execute('select execution_datetime from data_transformation_execution where (id >2)')
# list = select_times.fetchall()
# print(list)
# id = 2

# for i in list:
#     horario_datetime = datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S')
#     update_table = connection.cursor()
#     update_table.execute(f'UPDATE data_transformation_execution SET execution_datetime_end = \'{horario_datetime}\' WHERE id = {id}')
#     id = id+2
#     connection.commit()

# update_table = connection.cursor()
# update_table.execute('UPDATE data_transformation_execution SET program_id = 5 WHERE ((data_transformation_id = 6) AND (id >= 1) and (id <= 1163));')
# # update_table.fetchall()
# update_table.description
# connection.commit()

# update_table = connection.cursor()
# update_table.execute('UPDATE data_transformation_execution SET program_id = 4 WHERE ((data_transformation_id = 6) AND (id >= 1163) and (id <= 2326));')
# # update_table.fetchall()
# update_table.description
# connection.commit()

# update_table = connection.cursor()
# update_table.execute('UPDATE data_transformation_execution SET program_id = 6 WHERE ((data_transformation_id = 6) AND (id >= 2326) and (id <= 3489));')
# # update_table.fetchall()
# update_table.description
# connection.commit()

# update_table = connection.cursor()
# update_table.execute('UPDATE data_transformation_execution SET program_id = 4 WHERE ((data_transformation_id = 12) AND (id >= 3489) and (id <= 4652));')
# # update_table.fetchall()
# update_table.description
# connection.commit()

# update_table = connection.cursor()
# update_table.execute('UPDATE data_transformation_execution SET program_id = 5 WHERE ((data_transformation_id = 12) AND (id >= 4652) and (id <= 5815));')
# # update_table.fetchall()
# update_table.description
# connection.commit()

# update_table = connection.cursor()
# update_table.execute('UPDATE data_transformation_execution SET program_id = 6 WHERE ((data_transformation_id = 12) AND (id >= 5815) and (id <= 6978));')
# # update_table.fetchall()
# update_table.description
# connection.commit()

def time_average(ontoexpline, ontology_program, program_id):
    print("Calculando media de tempo: ", ontology_program, program_id)
    data_transformation_times = connection.cursor()
    data_transformation_times.execute(
        'select execution_datetime, execution_datetime_end from data_transformation_execution where program_id = %s ;' % (program_id))
    data_transformation_times = data_transformation_times.fetchall()
    print("***", data_transformation_times)

    time_total = datetime.strptime("0:00:00", '%H:%M:%S')
    average = datetime.strptime("0:00:00", '%H:%M:%S')
    qtd_times = 0
    interval_list = []

    for i in data_transformation_times:
        # print(i[0])
        time1 = datetime.strptime(str(i[0]), '%Y-%m-%d %H:%M:%S')
        time2 = datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S')
        interval = time2 - time1
        if (interval):
            print("interval: ", interval)
            print("time1: ", time1)
            print("time2: ", time2)
            time_total = time_total + interval
            interval_list.append(interval)
            # qtd_times+=1

    print("total time: ", time_total)
    print("qtds: ", qtd_times)

    # calculando a média de tempo do programa --> mandar pra ontoexpline na data property median_execution_time
    print("Media: ", statistics.median(interval_list))


    average = dateutil.parser.parse(str(statistics.median(interval_list)))
    print("=====> ",average.replace(microsecond=0))
    #reasoner da problema se nao tirar os microssegundos do datetime:
    ontology_program.timeAverage = average.replace(microsecond=0)
    print(ontology_program)
    ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")



def find_min_max_time(program, ontoexpline, program_id):
    data_transformation_times = connection.cursor()
    data_transformation_times.execute(
        'select execution_datetime, execution_datetime_end from data_transformation_execution where ((program_id = %s)) ;' % (
            program_id))
    data_transformation_times = data_transformation_times.fetchall()
    print("len lista:", len(data_transformation_times))

    time_total = datetime.strptime("00:00:00", '%H:%M:%S')
    interval_list = []

    for i in data_transformation_times:
        # print(i[0])
        time1 = datetime.strptime(str(i[0]), '%Y-%m-%d %H:%M:%S')
        time2 = datetime.strptime(str(i[1]), '%Y-%m-%d %H:%M:%S')

        interval = time2 - time1
        if (interval):
            print("interval: ", interval)
            # print("time1: ", time1)
            # print("time2: ", time2)
            time_total = time_total + interval
            interval_list.append(interval)
    print("--------------------------------------")
    print("total time: ", time_total)
    program.totalExecutionTime = time_total
    # minTime = datetime.strptime(min(interval_list), '%H:%M:%S')
    # maxTime = datetime.strptime(max(interval_list), '%H:%M:%S')
    minTime = datetime.strptime(str(min(interval_list)), '%H:%M:%S')
    maxTime = datetime.strptime(str(max(interval_list)), '%H:%M:%S')

    #combinando a data da execução com o total de tempo gasto na execução de tempo mínimo
    d = date(time1.year, time1.month, time1.day)
    t = time(minTime.hour, minTime.minute, minTime.second)
    minDateTime = datetime.combine(d, t)
    # calculando a média de tempo do programa --> mandar pra ontoexpline na data property median_execution_time
    print("--------------------------------------")
    print("min datetime: ", minDateTime)
    # print("max time: ", maxTime)
    program.hasMinExecutionTime = minDateTime

    # combinando a data da execução com o total de tempo gasto na execução de tempo máximo
    d = date(time1.year, time1.month, time1.day)
    t = time(maxTime.hour, maxTime.minute, maxTime.second)
    maxDateTime = datetime.combine(d, t)

    # calculando a média de tempo do programa --> mandar pra ontoexpline na data property median_execution_time
    print("--------------------------------------")
    print("max datetime: ", maxDateTime)
    program.hasMaxExecutionTime = maxDateTime


    # program.hasMaxExecutionTime = maxTime
    ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
def alter_telemetry():
    data_transformation = connection.cursor()
    data_transformation.execute(
        'select id, execution_datetime, execution_datetime_end from data_transformation_execution;')
    data_transformation = data_transformation.fetchall()

    telemetry = connection.cursor()
    telemetry.execute('select id, captured_timestamp, dt_execution_23  from telemetry;')
    telemetry = telemetry.fetchall()

    t = connection.cursor()
    t.execute('select * from telemetry where id >= 3318 and id < 3324;')
    t = t.fetchall()
    print(t)

    for f in telemetry:
        print(f[0], '\n')
        for i in data_transformation:
            # print(f[1])
            telemetry_time = parser.parse(f[1])
            dt_initial_time = parser.parse(i[1])

            # dt_final_time = parser.parse(i[2])

            # print(telemetry_time)
            # print(f[0])

            if ((telemetry_time >= dt_initial_time) and (telemetry_time <= i[2])):
                print("id da dt_execution: ", i[0], " telemetria", telemetry_time, " está no intervalo", i[1], i[2])

                up_telemetry = connection.cursor()
                up_telemetry.execute('UPDATE telemetry SET dt_execution_23 = %s WHERE (id = %s);' % (i[0], f[0]))
                # up_telemetry.fetchall()
                up_telemetry.description
                connection.commit()


def select_implementers_execution(data_transformation):
    implementers_execution = connection.cursor()
    implementers_execution.execute(
        'select id, program_id from data_transformation_execution where data_transformation_id = %s;' % data_transformation)
    implementers_execution = implementers_execution.fetchall()
    # print(implementers_execution)
    return implementers_execution


def find_data_tranformation_telemetry_metrics(data_transformation):
    implementers_execution = select_implementers_execution(data_transformation)
    scputimes_user = []
    scputimes_idle = []
    scputimes_steal = []

    # finding global data transformation CPU metrics
    for i in implementers_execution:
        id = i[0]
        select_telemetry = connection.cursor()
        select_telemetry.execute('select id from telemetry where dt_execution_23 = %s;' % id)
        select_telemetry = select_telemetry.fetchall()

        print("telemetria capturada: ", select_telemetry)

        for telemetry in select_telemetry:
            telemetry_cpu = connection.cursor()
            telemetry_cpu.execute(
                'select scputimes_user, scputimes_idle, scputimes_steal from telemetry_cpu where telemetry_id = %s; ' % telemetry)
            telemetry_cpu = telemetry_cpu.fetchall()

            # print("**** ", telemetry_cpu[0][0])
            scputimes_user.append(float(telemetry_cpu[0][0]))
            scputimes_idle.append(float(telemetry_cpu[0][1]))
            scputimes_steal.append(float(telemetry_cpu[0][2]))

    print("cpu telemetry number: ", len(scputimes_user))
    print("CPU user - transformation ", data_transformation, ": ", sum(scputimes_user) / len(scputimes_user))
    print("CPU idle - transformation ", data_transformation, ": ", sum(scputimes_idle) / len(scputimes_idle))
    print("CPU steal - transformation ", data_transformation, ": ", sum(scputimes_steal) / len(scputimes_steal))


def find_program_telemetry_metrics(program, ontoexpline):
    #program é um objeto ontológico
    program_name = program.name

    # program0= "mrbayes"
    implementer = connection.cursor()
    implementer.execute(f'select id from program where name = \'{program_name}\';')
    implementer = implementer.fetchall()
    print("** select do implementer: ", implementer[0])
    program_id = implementer[0][0]
    time_average(ontoexpline, program, program_id)
    find_min_max_time(program, ontoexpline, program_id)

    implementer_executions = connection.cursor()
    implementer_executions.execute(
        'select id, program_id from data_transformation_execution where program_id = %s;' % program_id)
    implementer_executions = implementer_executions.fetchall()

    #tempo de cpu
    scputimes_user = []
    scputimes_idle = []
    scputimes_steal = []

    #uso de RAM
    svmem_total = []
    svmem_available = []
    svmem_used = []

    #uso de disco
    sdiskio_read_bytes = []
    sdiskio_write_bytes = []
    sdiskio_busy_time = []

    # finding global data transformation CPU metrics
    for i in implementer_executions:
        id = i[0]
        # print("i: ", i)
        select_telemetry = connection.cursor()
        select_telemetry.execute('select id from telemetry where dt_execution_23 = %s;' % id)
        select_telemetry = select_telemetry.fetchall()
        # print("select telemetry: ", select_telemetry)

        if not select_telemetry:
            print("Execution ", i[0]," run by ",i[1], program, " has no telemetry.")
        else:
            print("The following telemetries was discovered to program ", program, ": ", select_telemetry)
            for telemetry in select_telemetry:
                telemetry_cpu = connection.cursor()
                telemetry_cpu.execute(
                    'select scputimes_user, scputimes_idle, scputimes_steal from telemetry_cpu where telemetry_id = %s; ' % telemetry)
                telemetry_cpu = telemetry_cpu.fetchall()

                # print("**** ", telemetry_cpu[0][0])
                scputimes_user.append(float(telemetry_cpu[0][0]))
                scputimes_idle.append(float(telemetry_cpu[0][1]))
                scputimes_steal.append(float(telemetry_cpu[0][2]))

                telemetry_memory = connection.cursor()
                telemetry_memory.execute(
                    'select svmem_total, svmem_available, svmem_used from telemetry_memory where telemetry_id = %s; ' % telemetry)
                telemetry_memory = telemetry_memory.fetchall()

                # print("**** ", telemetry_cpu[0][0])
                svmem_total.append(float(telemetry_memory[0][0]))
                svmem_available.append(float(telemetry_memory[0][1]))
                svmem_used.append(float(telemetry_memory[0][2]))

                telemetry_disk = connection.cursor()
                telemetry_disk.execute(
                    'select sdiskio_read_bytes, sdiskio_write_bytes, sdiskio_busy_time from telemetry_disk where telemetry_id = %s; ' % telemetry)
                telemetry_disk = telemetry_disk.fetchall()

                # print("**** ", telemetry_cpu[0][0])
                sdiskio_read_bytes.append(float(telemetry_disk[0][0]))
                sdiskio_write_bytes.append(float(telemetry_disk[0][1]))
                sdiskio_busy_time.append(float(telemetry_disk[0][2]))

            print("cpu telemetry number: ", len(scputimes_user))
            print("CPU user - program ", program, " (median): ", (sum(scputimes_user) / len(scputimes_user)))
            print("CPU idle - program ", program, " (median): ", (sum(scputimes_idle) / len(scputimes_idle)))
            print("CPU steal - program ", program, " (median): ", bytes2human(sum(scputimes_steal) / len(scputimes_steal)))
            program.hasUserCpu = (sum(scputimes_user) / len(scputimes_user))
            program.hasIdleTime = (sum(scputimes_idle) / len(scputimes_idle))

            print("--------------------------------------")
            print("memory telemetry number: ", len(scputimes_user))
            print("svmem_total - program ", program, " (median): ", bytes2human((sum(svmem_total) / len(svmem_total))))
            print("svmem_available - program ", program, " (median): ", bytes2human((sum(svmem_available) / len(svmem_available))))
            print("svmem_used - program ", program, " (median): ", bytes2human(sum(svmem_used) / len(svmem_used)))
            program.memoryUsageAverage = float(sum(svmem_used) / len(svmem_used))
            program.consumedMemory = bytes2human(sum(svmem_used) / len(svmem_used))
            program.hasMemoryAvailable = bytes2human(sum(svmem_available) / len(svmem_available))

            print("--------------------------------------")
            print("disk telemetry number: ", len(sdiskio_read_bytes))
            print("sdiskio_read_bytes - program ", program, " (median): ", bytes2human((sum(sdiskio_read_bytes) / len(sdiskio_read_bytes))))
            print("sdiskio_write_bytes - program ", program, " (median): ",
                  bytes2human((sum(sdiskio_write_bytes) / len(sdiskio_write_bytes))))
            print("sdiskio_busy_time - program ", program, " (median): ", bytes2human(sum(sdiskio_busy_time) / len(sdiskio_busy_time)))

            program.diskBusyTimeAverage = bytes2human(sum(sdiskio_busy_time) / len(sdiskio_busy_time))
            program.diskWriteBytesAverage = bytes2human((sum(sdiskio_write_bytes) / len(sdiskio_write_bytes)))
            program.diskReadBytesAverage = bytes2human((sum(sdiskio_write_bytes) / len(sdiskio_write_bytes)))

            ontoexpline.save(file="ontologies/ontoexpline.owl", format="rdfxml")
def search_program(program_name):
    program_information = connection.cursor()
    program_information.execute(
        f'select * from program where name = \'{program_name}\';')
    program_information = program_information.fetchall()
    return program_information

def search_data_transformation_by_program_exec(program_id):
    search_data_trans_exec = connection.cursor()
    search_data_trans_exec.execute(
        f'select dataflow_execution_id_2023 from data_transformation_execution where program_id = \'{program_id}\';')
    search_data_trans_exec = search_data_trans_exec.fetchall()
    return search_data_trans_exec

def search_data_transformation_by_expLine(activity_id):
    data_transformation_by_expLine = connection.cursor()
    data_transformation_by_expLine.execute(
        f'select dataflow_execution_id_2023 from data_transformation_execution where data_transformation_id = \'{activity_id}\';')
    data_transformation_by_expLine = data_transformation_by_expLine.fetchall()
    return data_transformation_by_expLine

def search_datatransformations_from_dataflow(dataflow_id):
    data_transformations = connection.cursor()
    data_transformations.execute(
        f'select data_transformation_id, data_transformation_id, program_id, dataflow_execution_id_2023  from data_transformation_execution where dataflow_execution_id_2023 = \'{dataflow_id}\';')
    data_transformations = data_transformations.fetchall()
    print(data_transformations)
    # return data_transformations

def get_df_id_from_data_transformation_execution(datatransformation_execution_id):
    dataflow_id = connection.cursor()
    dataflow_id.execute(
        f'select dataflow_execution_id_2023 from data_transformation_execution where id = \'{datatransformation_execution_id}\';')
    dataflow_id = dataflow_id.fetchall()
    return dataflow_id

def get_all_data_transformation_by_dataflow_id(dataflow_id):
    data_transformations = connection.cursor()
    data_transformations.execute(
        f'select id from data_transformation_execution where dataflow_execution_id_2023 = \'{dataflow_id}\';')
    data_transformations = data_transformations.fetchall()
    return(data_transformations)

    # return data_transformations
def search_data(ontoexpline, domain_operation, parametros):
    print("parâmetro de busca: ", parametros["model"])
    search = ontoexpline.search(type=ontoexpline.Program)
    for i in search:
        if (domain_operation in i.is_a):
            print("i:", i)
            program_infos = search_program(i.name)
            program_id = program_infos[0][0]
            print(program_id)

            dt_executions = search_data_transformation_by_program_exec(program_id)
            for dt in dt_executions:
                print("dataflow execution: ",dt)
                dt_in_dataflow = search_datatransformations_from_dataflow(dt[0])
                print(dt_in_dataflow, "\n")

            for att in parametros:
                search_att_occurrence = connection.cursor()
                search_att_occurrence.execute(
                    f'select id, {att} from ds_omodelgeneratormodule_raxml where {att} = \'{parametros[att]}\';')
                search_att_occurrence = search_att_occurrence.fetchall()
                print("**: ", search_att_occurrence)

def search_by_domain_operation(ontoexpline, operation, parameters):
        # 0 buscar quem implementa a operação
        search_program_op = ontoexpline.search(type=ontoexpline.Abstract_activity)
        print(search_program_op)
        dataflows_json = {"Dataflows": []}
        for item in search_program_op:
            if operation in item.is_a:
                print(item, item.hasId)
                print("** Out Relation: ", item.hasOutputRelation)
                for table in item.hasOutputRelation:
                    table = table.name

                for i in (list(set(parameters['attribute'].wasAssociatedWith))):
                    attribute = i

                search_task_id_in_db = connection.cursor()
                search_task_id_in_db.execute(
                        f'select id from task where dt_id = \'{item.hasId}\';')
                search_task_id_in_db = search_task_id_in_db.fetchall()
                print(search_task_id_in_db[0][0])

                attribute = attribute.name
                port_value = parameters['port_value']

                search_attribute_value_on_db = connection.cursor()
                search_attribute_value_on_db.execute(
                        f'select id, {attribute}, data_transformation_execution_id_2023 from {table} where modelgeneratormodule_raxml_task_id = \'{search_task_id_in_db[0][0]}\' and {attribute} = \'{port_value}\';')
                search_attribute_value_on_db = search_attribute_value_on_db.fetchall()
                print("** Table: ",table ," ids and occurence: ", search_attribute_value_on_db)
                # print(search_attribute_value_on_db[3][2])

                for occurence in search_attribute_value_on_db:
                    dataflows_id = get_df_id_from_data_transformation_execution(occurence[2])
                    for dataflow in dataflows_id:
                        print(f'** The model: {port_value}: was generated by Dataflow: {dataflow[0]} ', get_all_data_transformation_by_dataflow_id(dataflow[0]))
                        dataflows_json["Dataflows"].append(
                            {
                                "Domain_operation": operation.name,
                                "Dataflow_id": dataflow[0],
                                "Attribute:": attribute,
                                "Value": port_value,
                                "Data_transformations_execution_id:": get_all_data_transformation_by_dataflow_id(dataflow[0])
                            }
                        )
        with open("search_by_domain_operation.json", "w") as arquivo:
            json.dump(dataflows_json, arquivo, indent=3)










        # 1 buscar quem gera o atributo (data transformation e task)
        # 2 buscar qual dataflow executou ambos os implementadores estão




def up_df_execution():
    #os parametros devem ser alterados. existe um erro na tabela de data_Transformation_execution começa no id 4320, a dt 1 executou 3 vezes seguidas (erros de entrada)
    select_data = connection.cursor()
    select_data.execute(
        f'select id from data_transformation_execution where id >= 4350;')
    select_data = select_data.fetchall()
    print(select_data)

    i = 726
    for y in range (4348, 6976, 12):
        for dt in select_data:
            if (dt[0] > y) and (dt[0] <= y+12):
                print("i: ",i, "dt:     ", dt[0])
                up_data = connection.cursor()
                up_data.execute(f'UPDATE data_transformation_execution SET dataflow_execution_id_2023 = \'{i}\' WHERE id = {dt[0]}')
                connection.commit()
        i = i+2


def ds_omodelgeneratormodule_raxml():
    select_data = connection.cursor()
    select_data.execute(
        f'select id from data_transformation_execution where  data_transformation_id = 10;')
    select_data = select_data.fetchall()
    print(select_data)

    ds_o = connection.cursor()
    ds_o.execute(
        f'select id from ds_omodelgeneratormodule_raxml;')
    ds_o = ds_o.fetchall()
    for x in range (0, 292):
        print("inserir ", select_data[x][0], "no ds_o ", ds_o[x][0])
        update_table = connection.cursor()
        update_table.execute(f'UPDATE ds_omodelgeneratormodule_raxml SET data_transformation_execution_id_2023 = \'{select_data[x][0]}\' WHERE id = {ds_o[x][0]}')
        connection.commit()


# ds_omodelgeneratormodule_raxml()
# up_df_execution()
# find_data_tranformation_telemetry_metrics()
# find_program_telemetry_metrics()
# alter_telemetry()
# calculate_median_execution_time()
# find_min_max_time()