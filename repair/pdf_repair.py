from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from main.models import (Apartment, ApartmentDetail, Settings)
from tariff.models import Tariff
from datetime import datetime
from repair.models import CapitalRepair


def horizontalAlign(textLength, boxWidth, fontSize):
    horizontal_space = (boxWidth - (textLength * (fontSize / 2))) / 2
    return horizontal_space


def verticalAlign(boxHeight, row, allRow, offset):
    singleHeight = (boxHeight / allRow) * row
    vertical_space = offset - boxHeight + singleHeight
    return vertical_space - 2


def repair_generate_pdf():
    settings = Settings.objects.get(id=1)
    apartments = Apartment.objects.all()

    date_str = settings.month_to_date
    date_obj = datetime.strptime(date_str, '%d.%m.%Y')
    date_str = datetime.strftime(date_obj, '%d.%m.%Y')

    try:
        pdfmetrics.registerFont(
            TTFont('Calibri', r'/home/rainbowmzk/rainbow/static/fonts/calibri.ttf')
            )
        pdfmetrics.registerFont(
            TTFont('CalibriB', r'/home/rainbowmzk/rainbow/static/fonts/calibrib.ttf')
            )
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
        tariff = Tariff.objects.get(id=detail.tariff_id)
        repairData = CapitalRepair.objects.get(serialNumber=apartment.serialNumber)
        p.setFont("CalibriB", 10)
        p.drawString(20, h - 20 - y_offset, f'Дата печати {date_str}')
        p.setFont("Calibri", 10)
        fontSize = 10
        p.drawString(250, h - 20 - y_offset, 'Получатель платежа: ТСЖ"РАДУГА" ИНН 4214020636')
        p.drawString(20, h - 32 - y_offset, f'Счет квитанция № {apartment.serialNumber}')
        p.drawString(
            250, h - 32 - y_offset, 'КПП 421401001/БИК 043207612/Р.СЧЕТ 40705810426000000075'
            )
        p.drawString(20, h - 44 - y_offset, f'Плательщик взносов: {apartment.owner}')
        p.drawString(280, h - 44 - y_offset, '№ лицевого счета плательщика взносов для')
        p.drawString(340, h - 56 - y_offset, 'оплаты через Сбербанк:')
        p.drawString(370, h - 68 - y_offset, f'{detail.personalAccount}')
        p.drawString(20, h - 56 - y_offset, f'Период: {settings.month_name}')
        p.drawString(20, h - 68 - y_offset, f'Срок оплаты до: {settings.pay_up_to}')
        p.drawString(
            20, h - 80 - y_offset,
            f'Адрес г. Междуреченск пр. Шахтеров 55 кв. № {apartment.serialNumber}'
            )
        p.drawString(
            300, h - 80 - y_offset, f'Единый лицевой счет в ГИС ЖКХ: {detail.account_number}'
            )

        # Drawing header row || total width = 570
        start, offset, width, height = 15, 125, 80, 36
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Вид платежа'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 60
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Площадь,'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 2, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'кв.м.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 55
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Тариф,'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 2, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 80
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Задолженность'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'на начало'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'периода, руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 80
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Начислено за'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 2, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'период, руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 65
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Оплачено в'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'период,'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 65
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Пеня руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 85
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Итого'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'к оплате,'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'руб.'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing second row || total width = 570
        start, offset, width, height = 15, offset + 50, 80, 50
        p.rect(start, h - offset - y_offset, width, height)
        label = 'Минимальный'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 1, 4, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)
        label = 'взнос на'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'капитальный'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)
        label = 'ремонт'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = vertical_space - 10
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 60
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{detail.totalArea}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 55
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{tariff.capital_repair}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 80
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{repairData.debt}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 80
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{repairData.accrued()}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 65
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{repairData.paid}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 65
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{repairData.fine}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        start, width = width + start, 85
        p.rect(start, h - offset - y_offset, width, height)
        label = f'{repairData.total()}'
        horizontal_space = start + horizontalAlign(len(label), width, fontSize)
        vertical_space = h - verticalAlign(height, 2, 3, offset) - y_offset
        p.drawString(horizontal_space, vertical_space, label)

        # Drawing bottom
        p.drawString(
            20, h - 188 - y_offset, '*срок оплаты взноса на капитальный ремонт '
                                    'ежемесячно до 10 числа месяца следующего за '
                                    'расчетным (п.1 ст. 155 ЖК РФ)'
            )

        p.drawString(
            20, h - 200 - y_offset, 'По вопросам и оплате обращаться: г. Междуреченск, '
                                    'пр-т Шахтеров 55, 1й подъезд, 1й этаж, правление ТСЖ "РАДУГА"'
        )

        p.drawString(
            20, h - 212 - y_offset, 'Часы работы: понедельник и четверг с 18.00 до 20.00'
        )

        if apartment.serialNumber % 3 != 0:
            p.setFont("Calibri", 12)
            p.line(0, h - 220 - y_offset, 700, h - 220 - y_offset)
            y_offset += 220
        else:
            p.showPage()
            y_offset = 0
    p.save()

    # get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="repair_receipt.pdf"'
    response.write(pdf)
    return response
