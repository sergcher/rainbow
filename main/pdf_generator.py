from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from main.models import (Apartment, ApartmentCharge, ApartmentCounter,
                         ApartmentDetail, ApartmentFee, Settings)
from tariff.models import Tariff


def horizontalAlign(textLength, boxWidth, fontSize):
    horizontal_space = (boxWidth - (textLength * (fontSize / 2))) / 2
    return horizontal_space


def verticalAlign(boxHeight, row, allRow, offset):
    singleHeight = (boxHeight / allRow) * row
    vertical_space = offset - boxHeight + singleHeight
    return vertical_space - 2


def generate_pdf():
    settings = Settings.objects.get(id=1)
    apartments = Apartment.objects.all()

    #
    try:
        pdfmetrics.registerFont(TTFont('Calibri', r'/home/rainbowmzk/rainbow/static/fonts/calibri.ttf'))
        pdfmetrics.registerFont(TTFont('CalibriB', r'/home/rainbowmzk/rainbow/static/fonts/calibrib.ttf'))
    except Exception as e:
        pdfmetrics.registerFont(TTFont('Calibri', r'.\static\fonts\calibri.ttf'))
        pdfmetrics.registerFont(TTFont('CalibriB', r'.\static\fonts\calibrib.ttf'))
        print(e)

    buffer = BytesIO()
    w, h = A4

    y_offset = 0
    p = canvas.Canvas(buffer, pagesize=A4)

    for apartment in apartments:
        detail = ApartmentDetail.objects.get(serialNumber=apartment.serialNumber)
        apartment_fee = ApartmentFee.objects.get(serialNumber=apartment.serialNumber)
        apartment_counter = ApartmentCounter.objects.get(serialNumber=apartment.serialNumber)
        apartment_charge = ApartmentCharge.objects.get(serialNumber=apartment.serialNumber)
        tariff = Tariff.objects.get(id=detail.tariff_id)
        p.setFont("CalibriB", 12)
        p.drawString(20, h - 20 - y_offset, f"Платежный документ № {settings.bill}-{apartment.serialNumber}")
        p.drawString(250, h - 20 - y_offset, f"расчетный период {settings.month_name}")
        p.rect(15, h - 66 - y_offset,  570, 45)
        p.setFont("CalibriB", 10)
        p.drawString(20, h - 32 - y_offset, 'Получатель платежа ТСЖ "Радуга"        ИНН 4214020636       КПП 421401001')
        p.setFont("Calibri", 10)
        p.drawString(20, h - 42 - y_offset,
                     'Адрес: 652873, обл.Кемеровская, г. Междуреченск, пр-кт Шахтеров, 55. Тел. 8 (38475) 5-03-42')
        p.drawString(20, h - 52 - y_offset,
                     '№ банковского счета и банковские реквизиты: Кемеровское отделение № 8615 "ПАО Сбербанк России"')
        p.setFont("CalibriB", 10)
        p.drawString(20, h - 62 - y_offset,
                     'БИК 043207612     р/сч 40703810626070100299    к/сч 30101810200000000612')
        p.rect(15, h - 102 - y_offset, 570, 36)
        p.drawString(20, h - 75 - y_offset, f"Плательщик/собственник помещения        "
                                            f"{apartment.owner}                         Единый лицевой счет ГИС ЖКХ {detail.account_number}")
        p.setFont("Calibri", 10)
        p.drawString(20, h - 87 - y_offset,
                     f'Адрес: 652873, обл.Кемеровская, г. Междуреченск, пр-кт Шахтеров, 55. кв. 1                  № Лицевого счета {detail.personalAccount}')
        p.drawString(20, h - 99 - y_offset,
                     f'Площадь общая/м2 {detail.totalArea}           '
                     f'кол-во проживающих/зарегистрированных граждан      {detail.livedQt}/{detail.registredQt}')

        # Drawing header row
        p.setFont("CalibriB", 10)
        fontSize = 10

        start, offset, width, height = 15, 135, 115, 33
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Виды услуг'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Ед.изм.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        p.setFont("CalibriB", 8)
        fontSize = 10

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = 'норматив'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 2
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'потребле'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 2
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'ния КУ'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 2
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Объем'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 2, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'услуг'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Тариф/Размер'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 4
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'платы на кв.м.,'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 11
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 4
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Текущее'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'показание'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 4
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'счетчика - ИПУ'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 10
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Начислено за'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 4
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'расчетный'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 4
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'период/руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 4
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        p.setFont("CalibriB", 7)
        fontSize = 7

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Размер'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) - 2
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'повышающего'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) - 2
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'коэффициента'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) - 2
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        p.setFont("CalibriB", 8)
        fontSize = 8

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Перерасчеты'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 2, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'всего/руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        p.setFont("CalibriB", 7)
        fontSize = 7

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Всего к оплате'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize) + 2
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'за расчетный'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'период/руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing second row
        p.setFont("CalibriB", 10)
        fontSize = 10

        start, offset, width, height = 15, offset + 13, 520, 13
        p.rect(start, h - offset - y_offset, width, height)

        label = 'Коммунальные услуги итого:'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.maintenance_total}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing third row electricity
        p.setFont("Calibri", 10)
        fontSize = 10

        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Электроснабжение'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'кВт.ч'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_counter.electricity_value}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.electricity}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_counter.electricity_current}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.electricity}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_charge.recalculation_electricity}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.electricity + apartment_charge.recalculation_electricity}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing fourth row heating
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Отопление'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Гкал'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = '0.0176'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.heating}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.heating_rub}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.heating_rub}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{round(apartment_charge.recalculation_heating_rub, 2)}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{round(apartment_fee.heating_rub + apartment_charge.recalculation_heating_rub, 2)}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing fifth row hot water
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Горячее водоснабжение'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'куб.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = '3.37'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        if apartment_counter.hot_water_previous == 0 and apartment_counter.hot_water_current == 0:
            label = f'{detail.livedQt}'
        else:
            label = f'{apartment_counter.hot_water_value}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.hot_water}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_counter.hot_water_current}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.hot_water}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        if tariff.multiplying_factor == 1:
            label = '-'
        else:
            label = f'{tariff.multiplying_factor}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_charge.recalculation_hot_water}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.hot_water + apartment_charge.recalculation_hot_water}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing sixth row cold water
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Холодное водоснабжение'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'куб.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = '5.01'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        if apartment_counter.cold_water_previous == 0 and apartment_counter.cold_water_current == 0:
            label = f'{detail.livedQt}'
        else:
            label = f'{apartment_counter.cold_water_value}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.cold_water}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_counter.cold_water_current}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.cold_water}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        if tariff.multiplying_factor == 1:
            label = '-'
        else:
            label = f'{tariff.multiplying_factor}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_charge.recalculation_cold_water}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.cold_water + apartment_charge.recalculation_cold_water}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing seven row sewage
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Водоотведение'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'куб.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = '8.38'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        if apartment_counter.cold_water_previous == 0 and apartment_counter.cold_water_current == 0:
            label = f'{detail.livedQt}'
        else:
            label = f'{apartment_counter.wastewater_value}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.sewage}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_counter.wastewater_value}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.sewage}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_charge.recalculation_sewage}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.sewage + apartment_charge.recalculation_sewage}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing eight row solid waste
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Обращение с ТКО'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'чел.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = ''
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{detail.registredQt}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.solid_waste}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.solid_waste}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_charge.recalculation_solid_waste}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.solid_waste + apartment_charge.recalculation_solid_waste}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing nine row
        p.setFont("CalibriB", 10)
        fontSize = 10

        start, offset, width, height = 15, offset + 13, 520, 13
        p.rect(start, h - offset - y_offset, width, height)

        label = 'Плата за содержание помещения итого:'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.maintenance_full}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing ten row maintenance
        p.setFont("Calibri", 8)
        fontSize = 8

        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Содержание жилого помещения'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        p.setFont("Calibri", 10)
        fontSize = 10

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'кв.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = ''
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{detail.totalArea}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.maintenance}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.maintenance}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = '0'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.maintenance}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing eleven row electricity odn
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'ОДН электроэнергия'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'кв.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = ''
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{detail.totalArea}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.electricity_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.electricity_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = '0'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.electricity_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing twelve row sewage odn
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'ОДН сточные воды'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'кв.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = ''
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{detail.totalArea}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.sewage_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.sewage_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = '0'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.sewage_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing thirteen row cold water odn
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'ОДН холодная вода'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'кв.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = ''
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{detail.totalArea}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.cold_water_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.cold_water_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = '0'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.cold_water_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing fourteen row hot water odn
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'ОДН горячая вода'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'кв.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = ''
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{detail.totalArea}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.hot_water_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.hot_water_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = '0'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.hot_water_odn}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing fifteen row lift
        start, offset, width, height = 15, offset + 13, 115, 13
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Лифт   тех.обслуживание'
        horizontal_space = 17
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'кв.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = ''
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 40
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{detail.totalArea}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.lift}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 57
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.lift}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 54
        p.rect(start, h - offset - y_offset, width, height)
        label = '-'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = '0'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{apartment_fee.lift}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 1, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing total rows
        p.setFont("Calibri", 10)
        p.drawString(350, h - 327 - y_offset, r"Всего по услугам за расчетный период/руб.")
        p.line(538, h - 329 - y_offset, 585, h - 329 - y_offset)
        total_ = round(apartment_fee.maintenance_full + apartment_fee.maintenance_total, 2)
        p.drawString(540, h - 327 - y_offset, f'{total_}')
        p.drawString(315, h - 341 - y_offset, r"Задолженность на начало расчетного периода/руб.")
        p.line(538, h - 343 - y_offset, 585, h - 343 - y_offset)
        p.drawString(540, h - 341 - y_offset, f"{apartment_fee.balance_start}")
        p.drawString(473, h - 357 - y_offset, r"Оплачено/руб.")
        p.line(538, h - 359 - y_offset, 585, h - 359 - y_offset)
        p.drawString(540, h - 357 - y_offset, f"{apartment_fee.paid}")
        p.drawString(493, h - 371 - y_offset, r"Пени/руб.")
        p.line(538, h - 373 - y_offset, 585, h - 373 - y_offset)
        p.drawString(540, h - 371 - y_offset, f"{apartment_fee.fine}")
        p.setFont("CalibriB", 12)
        p.drawString(47, h - 385 - y_offset,
                     f"Итого к оплате на {settings.month_to_date} "
                     "(с учетом задолженности/переплаты за расчетный период) руб.")
        p.line(538, h - 387 - y_offset, 585, h - 387 - y_offset)
        p.drawString(540, h - 385 - y_offset, f"{apartment_fee.total}")
        if apartment.serialNumber % 2 != 0:
            p.setFont("Calibri", 12)
            p.line(0, h - 400 - y_offset, 700, h - 400 - y_offset)
            y_offset += 400
        else:
            p.showPage()
            y_offset = 0
    p.save()

    # get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="apartment_receipt.pdf"'
    response.write(pdf)
    return response
