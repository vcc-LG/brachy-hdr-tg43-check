import pyodbc


def connect_to_db():
    """Returns connection to OTP database on OTP server"""
    with open(r'hdrpackage\\server_config.cfg', 'r') as f:
        conn_string = f.read()
    return pyodbc.connect(conn_string)


def get_patient_cases(patient):
    """Returns list of cases for patient with specified ID"""
    # ----- Get database connection
    db = connect_to_db()
    try:
        c1 = db.cursor()
        try:
            c1.execute(
                """SELECT tc.SLABEL """
                """FROM BOM.PATIENT pt """
                """    INNER JOIN BOM.TCASE tc ON pt.SUID = tc.SPATIENTUID """
                """WHERE """
                """    pt.SID = '%s' """ %
                patient)
            res = c1.fetchall()
            cases = []
            for re in res:
                cases.append(re[0])
        finally:
            c1.close()
    finally:
        db.close()
    return cases


def get_plans_from_case(patient, case):
    """Returns list of plans for patient specified ID, case"""
    db = connect_to_db()
    try:
        c1 = db.cursor()
        try:
            query_str = \
                """SELECT rtplan.SLABEL """ \
                """FROM BOM.PATIENT pt """ \
                """    INNER JOIN BOM.TCASE tc ON pt.SUID = tc.SPATIENTUID """ \
                """ INNER JOIN BOM.RTPLAN rtplan ON rtplan.SCASEUID = tc.SUID """ \
                """ WHERE """ \
                """    pt.SID = '%s' AND """ \
                """    tc.SLABEL = '%s' """ % (patient, case)
            c1.execute(query_str)
            res = c1.fetchall()
            plans = []
            for re in res:
                plans.append(re[0])
        finally:
            c1.close()
    finally:
        db.close()
    return plans


def get_rtplan(
        patient,
        case,
        plan_string="",
        images=False,
        published=False):
    """Returns RT plan data for patient with specified ID, case, plan name"""
    db = connect_to_db()
    try:
        c1 = db.cursor()
        try:
            if not images:
                imagestr = " AND LOWER(rtplan.SLABEL) NOT LIKE '%image%' "
            else:
                imagestr = ""
            if published:
                pubstring = " AND rtplan.BHASDOSEMATRIX = 'T' AND rtplan.BPUBLISHED = 'T' "
            else:
                pubstring = ""
            if plan_string != "":
                plan_string = " AND (rtplan.SLABEL = '%s') " % plan_string
            querystr = """SELECT rtplan.SLABEL, rtplan.LBPART10BLOB """ \
                       """FROM BOM.PATIENT pt """ \
                       """    INNER JOIN BOM.TCASE tc ON pt.SUID = tc.SPATIENTUID """ \
                       """    INNER JOIN BOM.RTPLAN rtplan ON rtplan.SCASEUID = tc.SUID """ \
                       """WHERE """ \
                       """    pt.SID = '%s' and tc.SLABEL = '%s'""" % (
                           patient, case) + imagestr + pubstring + plan_string
            # print querystr
            c1.execute(querystr)

            res = c1.fetchall()

        finally:
            c1.close()
    finally:
        db.close()

    return res


def write_file(data, filename="RTSTRUCT.dcm"):
    """Write data to file"""
    file = open(filename, "wb")
    file.write(data)
    file.close()

if __name__ == '__main__':
    print("Ran as script")