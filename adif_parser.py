import os, pandas as pd, re

#modified from https://github.com/bjorgan/adif_parser
#designed to work only with QRZ.com exports

app_qrzlog_logid_COL = 'app_qrzlog_logid'
app_qrzlog_qsldate_COL = 'app_qrzlog_qsldate'
app_qrzlog_status_COL = 'app_qrzlog_status'
band_COL = 'band'
band_rx_COL = 'band_rx'
call_COL = 'call'
cnty_COL = 'cnty'
comment_COL = 'comment'
cont_COL = 'cont'
country_COL = 'country'
cqz_COL = 'cqz'
distance_COL = 'distance'
dxcc_COL = 'dxcc'
email_COL = 'email'
eqsl_qsl_rcvd_COL = 'eqsl_qsl_rcvd'
eqsl_qsl_sent_COL = 'eqsl_qsl_sent'
freq_COL = 'freq'
freq_rx_COL = ''
gridsquare_COL = 'gridsquare'
ituz_COL = 'ituz'
lat_COL = 'lat'
lon_COL = 'lon'
lotw_qsl_rcvd_COL = 'lotw_qsl_rcvd'
lotw_qsl_sent_COL = 'lotw_qsl_sent'
mode_COL = 'mode'
my_city_COL = 'my_city'
my_cnty_COL = 'my_cnty'
my_country_COL = 'my_country'
my_cq_zone_COL = 'my_cq_zone'
my_gridsquare_COL = 'my_gridsquare'
my_itu_zone_COL = 'my_itu_zone'
my_lat_COL = 'my_lat'
my_lon_COL = 'my_lon'
my_name_COL = 'my_name'
name_COL = 'name'
qrzcom_qso_upload_date_COL = 'qrzcom_qso_upload_date'
qrzcom_qso_upload_status_COL = 'qrzcom_qso_upload_status'
qsl_rcvd_COL = 'qsl_rcvd'
qsl_sent_COL = 'qsl_sent'
qso_date_COL = 'qso_date'
qso_date_off_COL = 'qso_date_off'
qth_COL = 'qth'
rst_rcvd_COL = 'rst_rcvd'
rst_sent_COL = 'rst_sent'
state_COL = 'state'
station_callsign_COL = 'station_callsign'
time_off_COL = 'time_off'
time_on_COL = 'time_on'
tx_pwr_COL = 'tx_pwr'

def extract_adif_column(adif_file, col):
    """
    Extract data column from ADIF file (e.g. 'OPERATOR' column).
    Parameters
    ----------
    adif_file: file object
        ADIF file opened using open().
    col: str
        Name of column (e.g. OPERATOR).
    Returns
    -------
    matches: list of str
        List of values extracted from the ADIF file.
    """
    pattern = re.compile(f'^.*<{col}:\d\d*>([^<]*)', re.IGNORECASE)
    matches = [re.match(pattern, line)
            for line in adif_file]
    matches = [line[1].strip() for line in matches if line is not None]
    adif_file.seek(0)

    if len(matches) > 0:
        return matches
    else:
        return None

def parse_adif(filename):
   #comment out unwanted rows
   #need a better way to handle rows that don't exist
    """
    Parse ADIF file into a pandas dataframe.  Currently tries to find operator,
    date, time and call fields. Additional fields can be specified.
    Parameters
    ----------
    filename: str
        Path to ADIF file.
    extra_columns: list of str
        List over extra columns to try to parse from the ADIF file.
    Returns
    -------
    df: Pandas DataFrame
        DataFrame containing parsed ADIF file contents.
    """

    df = pd.DataFrame()
    adif_file = open(filename, 'r', encoding="iso8859-1")

    try:
        df = pd.DataFrame({
               'app_qrzlog_logid': extract_adif_column(adif_file, app_qrzlog_logid_COL),
               #'app_qrzlog_qsldate': extract_adif_column(adif_file, app_qrzlog_qsldate_COL),
               #'app_qrzlog_status': extract_adif_column(adif_file, app_qrzlog_status_COL),
               'band': extract_adif_column(adif_file, band_COL),
               'band_rx': extract_adif_column(adif_file, band_rx_COL),
               'call': extract_adif_column(adif_file, call_COL),
               #'cnty': extract_adif_column(adif_file, cnty_COL),
               'comment': extract_adif_column(adif_file, comment_COL),
               'cont': extract_adif_column(adif_file, cont_COL),
               'country': extract_adif_column(adif_file, country_COL),
               'cqz': extract_adif_column(adif_file, cqz_COL),
               'distance': extract_adif_column(adif_file, distance_COL),
               'dxcc': extract_adif_column(adif_file, dxcc_COL),
               #'email': extract_adif_column(adif_file, email_COL),
               #'eqsl_qsl_rcvd': extract_adif_column(adif_file, eqsl_qsl_rcvd_COL),
               #'eqsl_qsl_sent': extract_adif_column(adif_file, eqsl_qsl_sent_COL),
               'freq': extract_adif_column(adif_file, freq_COL),
               'freq_rx': extract_adif_column(adif_file, freq_rx_COL),
               'gridsquare': extract_adif_column(adif_file, gridsquare_COL),
               'ituz': extract_adif_column(adif_file, ituz_COL),
               'lat': extract_adif_column(adif_file, lat_COL),
               'lon': extract_adif_column(adif_file, lon_COL),
               #'lotw_qsl_rcvd': extract_adif_column(adif_file, lotw_qsl_rcvd_COL),
               #'lotw_qsl_sent': extract_adif_column(adif_file, lotw_qsl_sent_COL),
               'mode': extract_adif_column(adif_file, mode_COL),
               'my_city': extract_adif_column(adif_file, my_city_COL),
               'my_cnty': extract_adif_column(adif_file, my_cnty_COL),
               'my_country': extract_adif_column(adif_file, my_country_COL),
               'my_cq_zone': extract_adif_column(adif_file, my_cq_zone_COL),
               'my_gridsquare': extract_adif_column(adif_file, my_gridsquare_COL),
               'my_itu_zone': extract_adif_column(adif_file, my_itu_zone_COL),
               'my_lat': extract_adif_column(adif_file, my_lat_COL),
               'my_lon': extract_adif_column(adif_file, my_lon_COL),
               #'my_name': extract_adif_column(adif_file, my_name_COL),
               #'name': extract_adif_column(adif_file, name_COL),
               'qrzcom_qso_upload_date': extract_adif_column(adif_file, qrzcom_qso_upload_date_COL),
               #'qrzcom_qso_upload_status': extract_adif_column(adif_file, qrzcom_qso_upload_status_COL),
               #'qsl_rcvd': extract_adif_column(adif_file, qsl_rcvd_COL),
               #'qsl_sent': extract_adif_column(adif_file, qsl_sent_COL),
               'qso_date': extract_adif_column(adif_file, qso_date_COL),
               'qso_date_off': extract_adif_column(adif_file, qso_date_off_COL),
               'qth': extract_adif_column(adif_file, qth_COL),
               'rst_rcvd': extract_adif_column(adif_file, rst_rcvd_COL),
               'rst_sent': extract_adif_column(adif_file, rst_sent_COL),
               #'state': extract_adif_column(adif_file, state_COL),
               'station_callsign': extract_adif_column(adif_file, station_callsign_COL),
               'time_off': extract_adif_column(adif_file, time_off_COL),
               'time_on': extract_adif_column(adif_file, time_on_COL),
               'tx_pwr': extract_adif_column(adif_file, tx_pwr_COL)
               })
    except:
        return None
    return df

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(parse_adif("test.adi"))

parse_adif("test.adi").to_csv('adi-test.csv', index=False)
