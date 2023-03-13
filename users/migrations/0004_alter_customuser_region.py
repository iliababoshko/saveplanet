# Generated by Django 4.1.7 on 2023-03-06 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='region',
            field=models.CharField(choices=[('1', 'Республика Адыгея'), ('2', 'Республика Башкортостан'), ('3', 'Республика Бурятия'), ('4', 'Республика Алтай'), ('5', 'Республика Дагестан'), ('6', 'Республика Ингушетия'), ('7', 'Кабардино-Балкарская Республика'), ('8', 'Республика Калмыкия'), ('9', 'Карачаево-Черкесская Республика'), ('10', 'Республика Карелия'), ('11', 'Республика Коми'), ('82', 'Республика Крым'), ('12', 'Республика Марий Эл'), ('13', 'Республика Мордовия'), ('14', 'Республика Саха (Якутия)'), ('15', 'Республика Северная Осетия-Алания'), ('16', 'Республика Татарстан'), ('17', 'Республика Тыва'), ('18', 'Удмуртская Республика'), ('19', 'Республика Хакасия'), ('20', 'Чеченская Республика'), ('21', 'Чувашская Республика'), ('22', 'Алтайский край'), ('75', 'Забайкальский край'), ('41', 'Камчатский край'), ('23', 'Краснодарский край'), ('24', 'Красноярский край'), ('59', 'Пермский край'), ('25', 'Приморский край'), ('26', 'Ставропольский край'), ('27', 'Хабаровский край'), ('28', 'Амурская область'), ('29', 'Архангельская область'), ('30', 'Астраханская область'), ('31', 'Белгородская область'), ('32', 'Брянская область'), ('33', 'Владимирская область'), ('34', 'Волгоградская область'), ('35', 'Вологодская область'), ('36', 'Воронежская область'), ('37', 'Ивановская область'), ('38', 'Иркутская область'), ('39', 'Калининградская область'), ('40', 'Калужская область'), ('42', 'Кемеровская область'), ('43', 'Кировская область'), ('44', 'Костромская область'), ('45', 'Курганская область'), ('46', 'Курская область'), ('47', 'Ленинградская область'), ('48', 'Липецкая область'), ('49', 'Магаданская область'), ('50', 'Московская область'), ('51', 'Мурманская область'), ('52', 'Нижегородская область'), ('53', 'Новгородская область'), ('54', 'Новосибирская область'), ('55', 'Омская область'), ('56', 'Оренбургская область'), ('57', 'Орловская область'), ('58', 'Пензенская область'), ('60', 'Псковская область'), ('61', 'Ростовская область'), ('62', 'Рязанская область'), ('63', 'Самарская область'), ('64', 'Саратовская область'), ('65', 'Сахалинская область'), ('66', 'Свердловская область'), ('67', 'Смоленская область'), ('68', 'Тамбовская область'), ('69', 'Тверская область'), ('70', 'Томская область'), ('71', 'Тульская область'), ('72', 'Тюменская область'), ('73', 'Ульяновская область'), ('74', 'Челябинская область'), ('76', 'Ярославская область'), ('77', 'г. Москва'), ('78', 'г. Санкт-Петербург'), ('92', 'г. Севастополь'), ('79', 'Еврейская автономная область'), ('83', 'Ненецкий АО'), ('86', 'ХМАО - Югра'), ('89', 'Ямало-Ненецкий АО'), ('93', 'Донецкая народная Республика'), ('95', 'Луганская народная Республика'), ('96', 'Запорожская область'), ('94', 'Херсонская область')], help_text='Выберите регион вашего проживания', max_length=255, null=True, verbose_name='Регион'),
        ),
    ]