from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from main.forms import *
import os


def generate_pdf():
    settings = Settings.objects.get(id=1)
    apartments = Apartment.objects.all()

    # Get the full path to the font file
    font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'calibri.ttf')

    # Register the font with PDFmetrics
    pdfmetrics.registerFont(TTFont('Calibri', font_path))

    # Get the full path to the bold font file
    bold_font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'calibrib.ttf')

    # Register the bold font with PDFmetrics
    pdfmetrics.registerFont(TTFont('CalibriB', bold_font_path))

    #pdfmetrics.registerFont(TTFont('Calibri', r'.\static\fonts\calibri.ttf'))
    #pdfmetrics.registerFont(TTFont('CalibriB', r'.\static\fonts\calibrib.ttf'))

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
        p.drawString(20, h - 32 - y_offset, f'Получатель платежа ТСЖ "Радуга"        ИНН 4214020636       КПП 421401001')
        p.setFont("Calibri", 10)
        p.drawString(20, h - 42 - y_offset,
                     f'Адрес: 652873, обл.Кемеровская, г. Междуреченск, пр-кт Шахтеров, 55. Тел. 8 (38475) 5-03-42')
        p.drawString(20, h - 52 - y_offset,
                     f'№ банковсокго счета и банковские реквизиты: Кемеровское отделение № 8615 "ПАО Сбербанк России"')
        p.setFont("CalibriB", 10)
        p.drawString(20, h - 62 - y_offset,
                     f'БИК 043207612     р/сч 40703810626070100299    к/сч 30101810200000000612')
        p.rect(15, h - 102 - y_offset, 570, 36)
        p.drawString(20, h - 75 - y_offset, f"Плательщик/собственник помещения        {apartment.owner}       № Лицевого счета {detail.personalAccount}")
        p.setFont("Calibri", 10)
        p.drawString(20, h - 87 - y_offset,
                     f'Адрес: 652873, обл.Кемеровская, г. Междуреченск, пр-кт Шахтеров, 55. кв. 1')
        p.drawString(20, h - 99 - y_offset,
                     f'Площадь общая/отапливаемая площадь/м2 {detail.totalArea}           кол-во проживающих граждан      {detail.livedQt}')

        #Drawing header row
        p.setFont("CalibriB", 10)
        p.rect(15, h - 135 - y_offset, 115, 33)
        p.drawString(47.5, h - 120 - y_offset, f"Виды услуг")
        p.rect(130, h - 135 - y_offset, 50, 33)
        p.drawString(138, h - 120 - y_offset, f"Ед.изм.")
        p.setFont("CalibriB", 8)
        p.rect(180, h - 135 - y_offset, 40, 33)
        p.drawString(182.5, h - 110 - y_offset, f"норматив")
        p.drawString(183.5, h - 120 - y_offset, f"потребле")
        p.drawString(186, h - 130 - y_offset, f"ния КУ")
        p.rect(220, h - 135 - y_offset, 40, 33)
        p.drawString(229.5, h - 115 - y_offset, f"Объем")
        p.drawString(231.5, h - 125 - y_offset, f"услуг")
        p.rect(260, h - 135 - y_offset, 57, 33)
        p.drawString(262, h - 110 - y_offset, f"Тариф/Размер")
        p.drawString(262, h - 120 - y_offset, f"платы на кв.м.,")
        p.drawString(280.5, h - 130 - y_offset, f"руб.")
        p.rect(317, h - 135 - y_offset, 57, 33)
        p.drawString(328, h - 110 - y_offset, f"Текущее")
        p.drawString(325, h - 120 - y_offset, f"показание")
        p.drawString(319, h - 130 - y_offset, f"счетчика - ИПУ")
        p.rect(374, h - 135 - y_offset, 57, 33)
        p.drawString(378, h - 110 - y_offset, f"Начислено за")
        p.drawString(381, h - 120 - y_offset, f"расчетный")
        p.drawString(379, h - 130 - y_offset, f"период/руб.")
        p.setFont("CalibriB", 7)
        p.rect(431, h - 135 - y_offset, 54, 33)
        p.drawString(447, h - 110 - y_offset, f"Размер")
        p.drawString(434, h - 120 - y_offset, f"повышающего")
        p.drawString(434, h - 130 - y_offset, f"коэффициента")
        p.setFont("CalibriB", 8)
        p.rect(485, h - 135 - y_offset, 50, 33)
        p.drawString(487, h - 115 - y_offset, f"Перерасчеты")
        p.drawString(487, h - 125 - y_offset, f"всего/руб.")
        p.rect(535, h - 135 - y_offset, 50, 33)
        p.setFont("CalibriB", 7)
        p.drawString(537, h - 110 - y_offset, f"Всего к оплате")
        p.drawString(537, h - 120 - y_offset, f"за расчетный")
        p.drawString(537, h - 130 - y_offset, f"период/руб.")

        #Drawing second row
        p.setFont("CalibriB", 10)
        p.rect(15, h - 148 - y_offset, 520, 13)
        p.drawString(17, h - 145 - y_offset, f"Коммунальные услуги итого:")
        p.rect(535, h - 148 - y_offset, 50, 13)
        p.drawString(537, h - 145 - y_offset, f"{apartment_fee.maintenance_total}")

        # Drawing third row electricity
        p.setFont("Calibri", 10)
        p.rect(15, h - 161 - y_offset, 115, 13)
        p.drawString(17, h - 158 - y_offset, f"Электроснабжение")
        p.rect(130, h - 161 - y_offset, 50, 13)
        p.drawString(142, h - 158 - y_offset, f"кВт.ч")
        p.rect(180, h - 161 - y_offset, 40, 13)
        p.rect(220, h - 161 - y_offset, 40, 13)
        p.drawString(230, h - 158 - y_offset, f"{apartment_counter.electricity_value}")
        p.rect(260, h - 161 - y_offset, 57, 13)
        p.drawString(275, h - 158 - y_offset, f"{tariff.electricity}")
        p.rect(317, h - 161 - y_offset, 57, 13)
        p.drawString(330, h - 158 - y_offset, f"{apartment_counter.electricity_current}")
        p.rect(374, h - 161 - y_offset, 57, 13)
        p.drawString(384, h - 158 - y_offset, f"{apartment_fee.electricity}")
        p.rect(431, h - 161 - y_offset, 54, 13)
        p.drawString(457, h - 158 - y_offset, f"-")
        p.rect(485, h - 161 - y_offset, 50, 13)
        p.drawString(503, h - 158 - y_offset, f"{apartment_charge.recalculation_electricity}")
        p.rect(535, h - 161 - y_offset, 50, 13)
        p.drawString(537, h - 158 - y_offset, f"{apartment_fee.electricity + apartment_charge.recalculation_electricity}")

        # Drawing fourth row heating
        p.setFont("Calibri", 10)
        p.rect(15, h - 174 - y_offset, 115, 13)
        p.drawString(17, h - 171 - y_offset, f"Отопление")
        p.rect(130, h - 174 - y_offset, 50, 13)
        p.drawString(142, h - 171 - y_offset, f"Гкал")
        p.rect(180, h - 174 - y_offset, 40, 13)
        p.drawString(182, h - 171 - y_offset, f"0.0176")
        p.rect(220, h - 174 - y_offset, 40, 13)
        p.drawString(230, h - 171 - y_offset, str(apartment_fee.heating))
        p.rect(260, h - 174 - y_offset, 57, 13)
        p.drawString(275, h - 171 - y_offset, str(tariff.heating_rub))
        p.rect(317, h - 174 - y_offset, 57, 13)
        p.drawString(330, h - 171 - y_offset, f"-")
        p.rect(374, h - 174 - y_offset, 57, 13)
        p.drawString(384, h - 171 - y_offset, str(apartment_fee.heating_rub))
        p.rect(431, h - 174 - y_offset, 54, 13)
        p.drawString(457, h - 171 - y_offset, f"-")
        p.rect(485, h - 174 - y_offset, 50, 13)
        p.drawString(503, h - 171 - y_offset, str(round(apartment_charge.recalculation_heating_rub,2)))
        p.rect(535, h - 174 - y_offset, 50, 13)
        p.drawString(537, h - 171 - y_offset, f"{round(apartment_fee.heating_rub + apartment_charge.recalculation_heating_rub, 2)}")

        # Drawing fifth row hot water
        p.setFont("Calibri", 10)
        p.rect(15, h - 187 - y_offset, 115, 13)
        p.drawString(17, h - 184 - y_offset, f"Горячее водоснабжение")
        p.rect(130, h - 187 - y_offset, 50, 13)
        p.drawString(142, h - 184 - y_offset, f"куб.м.")
        p.rect(180, h - 187 - y_offset, 40, 13)
        p.drawString(182, h - 184 - y_offset, f"3.37")
        p.rect(220, h - 187 - y_offset, 40, 13)
        p.drawString(230, h - 184 - y_offset, str(apartment_counter.hot_water_value))
        p.rect(260, h - 187 - y_offset, 57, 13)
        p.drawString(275, h - 184 - y_offset, str(tariff.hot_water))
        p.rect(317, h - 187 - y_offset, 57, 13)
        p.drawString(330, h - 184 - y_offset, str(apartment_counter.hot_water_current))
        p.rect(374, h - 187 - y_offset, 57, 13)
        p.drawString(384, h - 184 - y_offset, str(apartment_fee.hot_water))
        p.rect(431, h - 187 - y_offset, 54, 13)
        p.drawString(457, h - 184 - y_offset, f"-")
        p.rect(485, h - 187 - y_offset, 50, 13)
        p.drawString(503, h - 184 - y_offset, str(apartment_charge.recalculation_hot_water))
        p.rect(535, h - 187 - y_offset, 50, 13)
        p.drawString(537, h - 184 - y_offset, f"{apartment_fee.hot_water + apartment_charge.recalculation_hot_water}")

        # Drawing sixth row cold water
        p.setFont("Calibri", 9)
        p.rect(15, h - 200 - y_offset, 115, 13)
        p.drawString(17, h - 197 - y_offset, f"Холодное водоснабжение")
        p.rect(130, h - 200 - y_offset, 50, 13)
        p.drawString(142, h - 197 - y_offset, f"куб.м.")
        p.rect(180, h - 200 - y_offset, 40, 13)
        p.drawString(182, h - 197 - y_offset, f"5.01")
        p.rect(220, h - 200 - y_offset, 40, 13)
        p.drawString(230, h - 197 - y_offset, f"{apartment_counter.cold_water_value}")
        p.rect(260, h - 200 - y_offset, 57, 13)
        p.drawString(275, h - 197 - y_offset, f"{tariff.cold_water}")
        p.rect(317, h - 200 - y_offset, 57, 13)
        p.drawString(330, h - 197 - y_offset, f"{apartment_counter.cold_water_current}")
        p.rect(374, h - 200 - y_offset, 57, 13)
        p.drawString(384, h - 197 - y_offset, f"{apartment_fee.cold_water}")
        p.rect(431, h - 200 - y_offset, 54, 13)
        p.drawString(457, h - 197 - y_offset, f"-")
        p.rect(485, h - 200 - y_offset, 50, 13)
        p.drawString(503, h - 197 - y_offset, f"{apartment_charge.recalculation_cold_water}")
        p.rect(535, h - 200 - y_offset, 50, 13)
        p.drawString(537, h - 197 - y_offset, f"{apartment_fee.cold_water + apartment_charge.recalculation_cold_water}")

        # Drawing seven row sewage
        p.setFont("Calibri", 10)
        p.rect(15, h - 213 - y_offset, 115, 13)
        p.drawString(17, h - 210 - y_offset, f"Водоотведение")
        p.rect(130, h - 213 - y_offset, 50, 13)
        p.drawString(142, h - 210 - y_offset, f"куб.м.")
        p.rect(180, h - 213 - y_offset, 40, 13)
        p.drawString(182, h - 210 - y_offset, f"8.38")
        p.rect(220, h - 213 - y_offset, 40, 13)
        p.drawString(230, h - 210 - y_offset, f"{apartment_counter.wastewater_value}")
        p.rect(260, h - 213 - y_offset, 57, 13)
        p.drawString(275, h - 210 - y_offset, f"{tariff.sewage}")
        p.rect(317, h - 213 - y_offset, 57, 13)
        p.drawString(330, h - 210 - y_offset, f"{apartment_counter.wastewater_value}")
        p.rect(374, h - 213 - y_offset, 57, 13)
        p.drawString(384, h - 210 - y_offset, f"{apartment_fee.sewage}")
        p.rect(431, h - 213 - y_offset, 54, 13)
        p.drawString(457, h - 210 - y_offset, f"-")
        p.rect(485, h - 213 - y_offset, 50, 13)
        p.drawString(503, h - 210 - y_offset, f"{apartment_charge.recalculation_sewage}")
        p.rect(535, h - 213 - y_offset, 50, 13)
        p.drawString(537, h - 210 - y_offset, f"{apartment_fee.sewage + apartment_charge.recalculation_sewage}")

        # Drawing eight row solid waste
        p.setFont("Calibri", 10)
        p.rect(15, h - 226 - y_offset, 115, 13)
        p.drawString(17, h - 223 - y_offset, f"Обращение с ТКО")
        p.rect(130, h - 226 - y_offset, 50, 13)
        p.drawString(142, h - 223 - y_offset, f"чел.")
        p.rect(180, h - 226 - y_offset, 40, 13)
        p.rect(220, h - 226 - y_offset, 40, 13)
        p.drawString(230, h - 223 - y_offset, f"{detail.registredQt}")
        p.rect(260, h - 226 - y_offset, 57, 13)
        p.drawString(275, h - 223 - y_offset, f"{tariff.solid_waste}")
        p.rect(317, h - 226 - y_offset, 57, 13)
        p.drawString(330, h - 223 - y_offset, f"-")
        p.rect(374, h - 226 - y_offset, 57, 13)
        p.drawString(384, h - 223 - y_offset, f"{apartment_fee.solid_waste}")
        p.rect(431, h - 226 - y_offset, 54, 13)
        p.drawString(457, h - 223 - y_offset, f"-")
        p.rect(485, h - 226 - y_offset, 50, 13)
        p.drawString(503, h - 223 - y_offset, f"{apartment_charge.recalculation_solid_waste}")
        p.rect(535, h - 226 - y_offset, 50, 13)
        p.drawString(537, h - 223 - y_offset, f"{apartment_fee.solid_waste + apartment_charge.recalculation_solid_waste}")

        # Drawing nine row
        p.setFont("CalibriB", 10)
        p.rect(15, h - 239 - y_offset, 520, 13)
        p.drawString(17, h - 236 - y_offset, f"Плата за содержание помещения итого:")
        p.rect(535, h - 239 - y_offset, 50, 13)
        p.drawString(537, h - 236 - y_offset, f"{apartment_fee.maintenance_full}")

        # Drawing ten row maintenance
        p.setFont("Calibri", 8)
        p.rect(15, h - 252 - y_offset, 115, 13)
        p.drawString(17, h - 249 - y_offset, f"Содержание жилого помещения")
        p.rect(130, h - 252 - y_offset, 50, 13)
        p.setFont("Calibri", 10)
        p.drawString(142, h - 249 - y_offset, f"кв.м.")
        p.rect(180, h - 252 - y_offset, 40, 13)
        p.rect(220, h - 252 - y_offset, 40, 13)
        p.drawString(230, h - 249 - y_offset, f"{detail.totalArea}")
        p.rect(260, h - 252 - y_offset, 57, 13)
        p.drawString(275, h - 249 - y_offset, f"{tariff.maintenance}")
        p.rect(317, h - 252 - y_offset, 57, 13)
        p.drawString(330, h - 249 - y_offset, f"-")
        p.rect(374, h - 252 - y_offset, 57, 13)
        p.drawString(384, h - 249 - y_offset, f"{apartment_fee.maintenance}")
        p.rect(431, h - 252 - y_offset, 54, 13)
        p.drawString(457, h - 249 - y_offset, f"-")
        p.rect(485, h - 252 - y_offset, 50, 13)
        p.drawString(503, h - 249 - y_offset, f"0")
        p.rect(535, h - 252 - y_offset, 50, 13)
        p.drawString(537, h - 249 - y_offset, f"{apartment_fee.maintenance}")

        # Drawing eleven row electricity odn
        p.setFont("Calibri", 10)
        p.rect(15, h - 265 - y_offset, 115, 13)
        p.drawString(17, h - 262 - y_offset, f"ОДН электроэнергия")
        p.rect(130, h - 265 - y_offset, 50, 13)
        p.drawString(142, h - 262 - y_offset, f"кв.м.")
        p.rect(180, h - 265 - y_offset, 40, 13)
        p.rect(220, h - 265 - y_offset, 40, 13)
        p.drawString(230, h - 262 - y_offset, f"{detail.totalArea}")
        p.rect(260, h - 265 - y_offset, 57, 13)
        p.drawString(275, h - 262 - y_offset, f"{tariff.electricity_odn}")
        p.rect(317, h - 265 - y_offset, 57, 13)
        p.drawString(330, h - 262 - y_offset, f"-")
        p.rect(374, h - 265 - y_offset, 57, 13)
        p.drawString(384, h - 262 - y_offset, f"{apartment_fee.electricity_odn}")
        p.rect(431, h - 265 - y_offset, 54, 13)
        p.drawString(457, h - 262 - y_offset, f"-")
        p.rect(485, h - 265 - y_offset, 50, 13)
        p.drawString(503, h - 262 - y_offset, f"0")
        p.rect(535, h - 265 - y_offset, 50, 13)
        p.drawString(537, h - 262 - y_offset, f"{apartment_fee.electricity_odn}")

        # Drawing twelve row sewage odn
        p.setFont("Calibri", 10)
        p.rect(15, h - 278 - y_offset, 115, 13)
        p.drawString(17, h - 275 - y_offset, f"ОДН сточные воды")
        p.rect(130, h - 278 - y_offset, 50, 13)
        p.drawString(142, h - 275 - y_offset, f"кв.м.")
        p.rect(180, h - 278 - y_offset, 40, 13)
        p.rect(220, h - 278 - y_offset, 40, 13)
        p.drawString(230, h - 275 - y_offset, f"{detail.totalArea}")
        p.rect(260, h - 278 - y_offset, 57, 13)
        p.drawString(275, h - 275 - y_offset, f"{tariff.sewage_odn}")
        p.rect(317, h - 278 - y_offset, 57, 13)
        p.drawString(330, h - 275 - y_offset, f"-")
        p.rect(374, h - 278 - y_offset, 57, 13)
        p.drawString(384, h - 275 - y_offset, f"{apartment_fee.sewage_odn}")
        p.rect(431, h - 278 - y_offset, 54, 13)
        p.drawString(457, h - 275 - y_offset, f"-")
        p.rect(485, h - 278 - y_offset, 50, 13)
        p.drawString(503, h - 275 - y_offset, f"0")
        p.rect(535, h - 278 - y_offset, 50, 13)
        p.drawString(537, h - 275 - y_offset, f"{apartment_fee.sewage_odn}")

        # Drawing thirteen row cold water odn
        p.setFont("Calibri", 10)
        p.rect(15, h - 291 - y_offset, 115, 13)
        p.drawString(17, h - 288 - y_offset, f"ОДН холодная вода")
        p.rect(130, h - 291 - y_offset, 50, 13)
        p.drawString(142, h - 288 - y_offset, f"кв.м.")
        p.rect(180, h - 291 - y_offset, 40, 13)
        p.rect(220, h - 291 - y_offset, 40, 13)
        p.drawString(230, h - 288 - y_offset, f"{detail.totalArea}")
        p.rect(260, h - 291 - y_offset, 57, 13)
        p.drawString(275, h - 288 - y_offset, f"{tariff.cold_water_odn}")
        p.rect(317, h - 291 - y_offset, 57, 13)
        p.drawString(330, h - 288 - y_offset, f"-")
        p.rect(374, h - 291 - y_offset, 57, 13)
        p.drawString(384, h - 288 - y_offset, f"{apartment_fee.cold_water_odn}")
        p.rect(431, h - 291 - y_offset, 54, 13)
        p.drawString(457, h - 288 - y_offset, f"-")
        p.rect(485, h - 291 - y_offset, 50, 13)
        p.drawString(503, h - 288 - y_offset, f"0")
        p.rect(535, h - 291 - y_offset, 50, 13)
        p.drawString(537, h - 288 - y_offset, f"{apartment_fee.cold_water_odn}")

        # Drawing fourteen row hot water odn
        p.setFont("Calibri", 10)
        p.rect(15, h - 304 - y_offset, 115, 13)
        p.drawString(17, h - 301 - y_offset, f"ОДН горячая вода")
        p.rect(130, h - 304 - y_offset, 50, 13)
        p.drawString(142, h - 301 - y_offset, f"кв.м.")
        p.rect(180, h - 304 - y_offset, 40, 13)
        p.rect(220, h - 304 - y_offset, 40, 13)
        p.drawString(230, h - 301 - y_offset, f"{detail.totalArea}")
        p.rect(260, h - 304 - y_offset, 57, 13)
        p.drawString(275, h - 301 - y_offset, f"{tariff.hot_water_odn}")
        p.rect(317, h - 304 - y_offset, 57, 13)
        p.drawString(330, h - 301 - y_offset, f"-")
        p.rect(374, h - 304 - y_offset, 57, 13)
        p.drawString(384, h - 301 - y_offset, f"{apartment_fee.hot_water_odn}")
        p.rect(431, h - 304 - y_offset, 54, 13)
        p.drawString(457, h - 301 - y_offset, f"-")
        p.rect(485, h - 304 - y_offset, 50, 13)
        p.drawString(503, h - 301 - y_offset, f"0")
        p.rect(535, h - 304 - y_offset, 50, 13)
        p.drawString(537, h - 301 - y_offset, f"{apartment_fee.hot_water_odn}")

        # Drawing fifteen row lift
        p.setFont("Calibri", 10)
        p.rect(15, h - 317 - y_offset, 115, 13)
        p.drawString(17, h - 314 - y_offset, f"Лифт   тех.обслуживание")
        p.rect(130, h - 317 - y_offset, 50, 13)
        p.drawString(142, h - 314 - y_offset, f"кв.м.")
        p.rect(180, h - 317 - y_offset, 40, 13)
        p.rect(220, h - 317 - y_offset, 40, 13)
        p.drawString(230, h - 314 - y_offset, f"{detail.totalArea}")
        p.rect(260, h - 317 - y_offset, 57, 13)
        p.drawString(275, h - 314 - y_offset, f"{tariff.lift}")
        p.rect(317, h - 317 - y_offset, 57, 13)
        p.drawString(330, h - 314 - y_offset, f"-")
        p.rect(374, h - 317 - y_offset, 57, 13)
        p.drawString(384, h - 314 - y_offset, f"{apartment_fee.lift}")
        p.rect(431, h - 317 - y_offset, 54, 13)
        p.drawString(457, h - 314 - y_offset, f"-")
        p.rect(485, h - 317 - y_offset, 50, 13)
        p.drawString(503, h - 314 - y_offset, f"0")
        p.rect(535, h - 317 - y_offset, 50, 13)
        p.drawString(537, h - 314 - y_offset, f"{apartment_fee.lift}")

        # Drawing total rows
        p.setFont("Calibri", 10)
        p.drawString(350, h - 327 - y_offset, f"Всего по услугам за расчетный период/руб.")
        p.line(538, h - 329 - y_offset, 585, h - 329 - y_offset)
        p.drawString(540, h - 327 - y_offset, f"{round(apartment_fee.maintenance_full + apartment_fee.maintenance_total, 2)}")
        p.drawString(315, h - 341 - y_offset, f"Задолженность на начало расчетного периода/руб.")
        p.line(538, h - 343 - y_offset, 585, h - 343 - y_offset)
        p.drawString(540, h - 341 - y_offset, f"{apartment_fee.balance_start}")
        p.drawString(473, h - 357 - y_offset, f"Оплачено/руб.")
        p.line(538, h - 359 - y_offset, 585, h - 359 - y_offset)
        p.drawString(540, h - 357 - y_offset, f"{apartment_fee.paid}")
        p.drawString(493, h - 371 - y_offset, f"Пени/руб.")
        p.line(538, h - 373 - y_offset, 585, h - 373 - y_offset)
        p.drawString(540, h - 371 - y_offset, f"{apartment_fee.fine}")
        p.setFont("CalibriB", 12)
        p.drawString(47, h - 385 - y_offset, f"Итого к оплате на {settings.month_to_date} (с учетом задолженности/переплаты за расчетный период) руб.")
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
