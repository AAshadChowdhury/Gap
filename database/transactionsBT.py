from database import config
# import alpaca_trade_api as tradeapi
import pymssql
import pandas as pd
import warnings


def ConnectDB(dbName='dbTrade'):
    try:
        connect = pymssql.connect(
            config.serverNameBT, config.userNameBT, config.passwordBT, dbName)
        # print('Database server connection successful.')
        return connect
    except Exception as e:
        # print(e)
        print('Database server connection failed.')
        raise(e)


def fncGetDataAsList(sqlQuery, dbName='dbTrade'):
    try:
        connect = ConnectDB(dbName)
        if connect is not None:
            cursor = connect.cursor()
            cursor.execute(sqlQuery)
            result = cursor.fetchall()
            return result
    except:
        return None
    finally:
        connect.close()


def fncGetDataAsPanda(sqlQuery, dbName='dbTrade'):
    try:
        connect = ConnectDB(dbName)
        if connect is not None:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                SQL_Query = pd.read_sql_query(sqlQuery, connect)
                df = pd.DataFrame(SQL_Query)
                # print(df) 
                return df
    except:
        return None
    finally:
        connect.close()


def fncGetDataAsDictionary(sqlQuery, dbName='dbTrade'):
    try:
        connect = ConnectDB(dbName)
        resultset = []

        if connect is not None:
            cursor = connect.cursor()

            cursor.execute(sqlQuery)
            columnNames = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            for row in rows:
                resultset.append(dict(zip(columnNames, row)))

            return resultset
    except Exception as e:
        raise(e)
    finally:
        cursor.close()
        connect.close()


def fncSaveData(sqlHeads, sqlData, dbName='dbTrade'):
    try:
        connect = ConnectDB(dbName)
        if connect is not None:
            cursor = connect.cursor()
            cursor.execute(sqlHeads, sqlData)
            connect.commit()
    except Exception as e:
        raise(e)
    finally:
        cursor.close()
        connect.close()


def fncUpdateData(sqlQuery, dbName="dbTrade"):
    try:
        connect = ConnectDB(dbName)
        if connect is not None:
            cursor = connect.cursor()
            cursor.execute(sqlQuery)
            connect.commit()
    except Exception as e:
        raise(e)
    finally:
        cursor.close()
        connect.close()


def fncProcessData(sqlQuery, dbName="dbTrade"):
    try:
        connect = ConnectDB(dbName)
        if connect is not None:
            cursor = connect.cursor()
            cursor.execute(sqlQuery)
            connect.commit()
    except Exception as e:
        raise(e)
    finally:
        cursor.close()
        connect.close()



# api=tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)

# assets=api.list_assets()

