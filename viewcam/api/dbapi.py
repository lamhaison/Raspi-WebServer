__author__ = 'root'

import MySQLdb
import json
import sys
import os
import commands
import time
from viewcam.viewmodel import device
from django.conf import settings

import logging
logger = logging.getLogger(__name__)


def exe_query(cursor, query):

    """
    execute query with try catch exception
    :param connect: cursor of connection
    :param query: data query
    :return:Resutl of query
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as detail:
        logger.debug("Error Query : %s" % query)
        logger.debug("Error detail: %s" % detail)
        return None


def create_connection_to_database():
    """
    Create connection to access database with configuration in setting file
    :return: return cursor of new database
    """
    try:
        connection = MySQLdb.connect( settings.CONNECTION_URL, # your host, usually localhost
                         settings.CONNECTION_USER, # your username
                         settings.CONNECTION_PASSWORD, # your password
                         settings.CONNECTION_DB_NAME) # name of the data base

        cur_connection = connection.cursor()
        return cur_connection
    except Exception as ex:
        logger.debug(ex)


def get_all_device():

    """
    Get all device in database
    :return:List all device
    """

    sql_query = "select * from devices"
    return exe_query(create_connection_to_database(), sql_query)

















