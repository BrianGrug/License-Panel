from django.db import models

from license_django import settings


class LicenseHelper:

    @staticmethod
    def get_collection(software):
        print(software)
        if software == "staffmode":
            return settings.MONGO_DATABASE.staffmode_licenses
        elif software == "zhub":
            return settings.MONGO_DATABASE.zhub_licenses
        elif software == "chronium":
            return settings.MONGO_DATABASE.chronium_licences
        elif software == "core":
            return settings.MONGO_DATABASE.core_licenses
        elif software == "pearls":
            return settings.MONGO_DATABASE.pearls_licenses
        elif software == "hub":
            return settings.MONGO_DATABASE.hub_licenses
        else:
            return None

    @staticmethod
    def license_exists(key, software):
        return LicenseHelper.get_collection(software).find_one({"key": key}) is not None

    @staticmethod
    def discord_exists(discord, software):
        return LicenseHelper.get_collection(software).find_one({"discord": discord}) is not None

    @staticmethod
    def get_discord(discord, software):
        return LicenseHelper.get_collection(software).find_one({"discord": discord}).get('key')


    @staticmethod
    def get_discord_license(key, software):
        if LicenseHelper.get_collection(software).find_one({"key": key}) is not None:
            return LicenseHelper.get_collection(software).find_one({"key": key})['discord']
        else:
            return "Invalid"

    @staticmethod
    def get_logs():
        logs = []
        docs = settings.MONGO_DATABASE.license_logs.find().limit(30)

        for doc in docs:
            logs.append({"date": doc['date'], "ip": doc['ip'], "key": doc['key'], "discord": doc['discord'], "software": doc['software']})

        return logs
