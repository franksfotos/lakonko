# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request as req
import random

REQUEST = 0
SUCCESS = 0
ERROR = 0
url = 'http://calculator.volkswagenbank.de/CalculatorFE/Services/XmlService.ashx'


def last_element(soup, tag):
    return soup.find_all(tag)[-1]


def get_xml_random_request():
    req_soup = BeautifulSoup(features='xml')

    # Request Tag
    req_soup.append(req_soup.new_tag('Request'))
    tag_request = req_soup.Request
    tag_request['Name'] = 'Defaults'
    tag_request['Domain'] = 'VW.NEW'
    tag_request['ResponsePassThru'] = 0

    # Product Tag
    tag_request.append(req_soup.new_tag('Product'))
    tag_product = req_soup.Product
    product_pool = ['CC', 'AC']
    tag_product['ID'] = random.choice(product_pool)

    # ProductParameters
    tag_product.append(req_soup.new_tag('Parameter'))
    tag_parameter = last_element(req_soup, 'Parameter')
    tag_parameter['ID'] = 'Duration'
    duration_pool = ['12', '24', '36']
    tag_parameter.string = random.choice(duration_pool)

    tag_product.append(req_soup.new_tag('Parameter'))
    tag_parameter = last_element(req_soup, 'Parameter')
    tag_parameter['ID'] = 'DownPayment'

    tag_DownPaymentPool = random.randint(0, 50)
    tag_parameter.string = str(tag_DownPaymentPool)

    tag_product.append(req_soup.new_tag('Parameter'))
    tag_parameter = last_element(req_soup, 'Parameter')
    tag_parameter['ID'] = 'RSV'
    tag_parameter.string = ("RSV")

    # Vehicle Tag
    tag_request.append(req_soup.new_tag('Vehicle'))
    tag_Vehicle = req_soup.Vehicle
    tag_Vehicle['Type'] = 'New'

    # Key Tag
    tag_Vehicle.append(req_soup.new_tag('Key'))
    tag_Key = req_soup.Key
    tag_Key.string = '1T322X'

    # Year Tag
    tag_Vehicle.append(req_soup.new_tag('Year'))
    tag_Year = req_soup.Year
    tag_Year.string = '2012'

    # PriceTotal Tag
    tag_Vehicle.append(req_soup.new_tag('PriceTotal'))
    tag_PriceTotal = req_soup.PriceTotal
    tag_PriceTotal.string = '30000'

    xml_data = str(req_soup).encode('utf-8')

    return xml_data


# print(xml_data)

# xml_data = """<Request Name="Defaults" Domain="VW.NEW" ResponsePassThru="0">
#  <!--Request0138.xml-->
#  <Product ID="CC">
#    <Parameter ID="Duration">48</Parameter>
#    <Parameter ID="DownPayment">8355</Parameter>
#    <Parameter ID="RSV">RSVPLUS</Parameter>
#  </Product>
#  <Vehicle Type="New">
#    <Key>5G13EX/EA7/E0P/WAL/ZBE</Key>
#    <Year>2017</Year>
#    <PriceModel>27850</PriceModel>
#    <PriceTotal>27850</PriceTotal>
#    <PriceOriginal>0</PriceOriginal>
#  </Vehicle>
# </Request>
# """.encode('utf8')

# opener = req.build_opener(proxy, auth, req.HTTPHandler)
# req.install_opener(opener)


def send_request(xml_data, url):
    global REQUEST
    global SUCCESS
    global ERROR

    conn = req.urlopen(url, data=xml_data)
    return_str = conn.read()
    REQUEST += 1

    soup = BeautifulSoup(return_str, 'xml')

    soup_error = soup.Error

    # None wenn kein Fehler vorliegt...
    if soup_error is not None:
        xml_response = soup_error.Description
        ERROR += 1
    else:
        rate_param = soup.findAll("Parameter", {"ID": "Rate"})
        xml_response = None
        xml_response = rate_param[0].Data.string
        SUCCESS += 1
    return xml_response


for x in range(100):
    xml = get_xml_random_request()

    response = send_request(get_xml_random_request(), url)

    if response != None:
        print(REQUEST, SUCCESS, ERROR, response)
