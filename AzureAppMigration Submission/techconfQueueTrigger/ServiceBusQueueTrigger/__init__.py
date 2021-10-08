import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime


def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode("utf-8"))
    logging.info(
        "Python ServiceBus queue trigger processed message: %s", notification_id
    )
    conn = None
    try:
        # Get connection to database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres@techconfdbserver",
            password="removed",
            host="techconfdbserver.postgres.database.azure.com",
        )
        cur = conn.cursor()
        # Get attendees email and name
        cur.execute("SELECT first_name, last_name, email FROM attendee;")
        attendees = cur.fetchall()
        compDate = datetime.now()
        # Update Completion Date
        cur.execute(
            'UPDATE "notification" SET "completed_date"=%s WHERE "id"=%s;',
            (compDate, notification_id),
        )
        # Update Number of Attendees
        status = "Notified {} attendees".format(len(attendees))
        cur.execute(
            'UPDATE "notification" SET "status"=%s WHERE "id"=%s;',
            (status, notification_id),
        )
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()
            print("Database connection closed.")
