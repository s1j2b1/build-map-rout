
import csv
import math
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


from flask import Flask, render_template, request
# استدعي كلاساتك هنا (GoogleMapsScraper, RouteOptimizer, إلخ)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indexx.html')

def arab_txt(text):
    import arabic_reshaper
    from bidi.algorithm import get_display
    reshaped = arabic_reshaper.reshape(text) # يرتّب الحروف داخل الكلمة (shaping)  
    bidi_text = get_display(reshaped)        # يعدّل الاتجاه للعرض في بيئة LTR
    return bidi_text
print(arab_txt('اعوذ بالله من الشيطان الرجيم'))

@app.route('/generate', methods=['POST'])
def generate():
    # هنا تضع منطق الكود الخاص بك:
    # 1. استخراج البيانات
    # 2. ترتيب المسار




    # =====================================================================
    # المرحلة الأولى: كلاس استخراج البيانات وأتمتة المتصفح (Web Scraping)
    # =====================================================================
    class GoogleMapsScraper:
        print("i am sulaiman 00")
        """كلاس مسؤول عن أتمتة متصفح كروم، الدخول إلى خرائط جوجل، واستخراج الإحداثيات جغرافياً."""

        def __init__(self, user_data_dir: str, profile_dir: str = "Default"):
            print("i am sulaiman 0")

            """تهيئة إعدادات المتصفح باستخدام ملف تعريف المستخدم الحالي لتفادي تسجيل الدخول."""
            self.options = Options()
            # تمرير مسار ملف تعريف المستخدم لفتح المتصفح بجلسة العمل النشطة (Cookies & Login)
            self.options.add_argument(f"--user-data-dir={user_data_dir}")
            self.options.add_argument(f"--profile-directory={profile_dir}")
            self.options.add_argument(
                "--start-maximized"
            )  # فتح المتصفح بكامل الشاشة
            self.options.add_argument(
                "--disable-blink-features=AutomationControlled"
            )  # إخفاء أثر الأتمتة لمنع الحظر
            self.driver = None

        def start_driver(self):
            print("i am sulaiman 1")

            """بدء تشغيل متصفح كروم بالاعتماد على WebDriverManager."""
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=self.options)
                print(arab_txt("[+] تم تشغيل المتصفح بنجاح باستخدام ملف التعريف الخاص بك."))
            except Exception as e:
                print(arab_txt(f"[-] خطأ أثناء تشغيل المتصفح: {e}"))
                raise e

        def extract_coords_from_url(self, url: str) -> tuple:
            print("i am sulaiman 2")
            """تحليل الرابط النهائي لاستخراج خطوط الطول والعرض عبر التعبيرات النمطية (Regex)."""
            # النمط الشهير لخرائط جوجل الذي يحتوي على الإحداثيات بعد علامة @
            regex_pattern = r"@([-+]?\d+\.\d+),([-+]?\d+\.\d+)"
            match = re.search(regex_pattern, url)

            if match:
                lat = float(match.group(1))
                lng = float(match.group(2))
                return lat, lng
            return None, None

        def scrape_saved_list(self, list_url: str, output_csv: str = "locations.csv"):
            print("i am sulaiman 3")

            """الدخول إلى قائمة الأماكن المحفوظة، زيارة كل موقع، واستخراج بياناته إلى ملف CSV."""
            if not self.driver:
                self.start_driver()

            try:
                print("i am sulaiman 4")

                print(arab_txt(f"[+] جاري الانتقال إلى رابط القائمة المحفوظة: {list_url}"))
                self.driver.get(list_url)
                time.sleep(5)  # وقت مستقطع لضمان تحميل القائمة بالكامل

                # استخراج روابط المواقع الموجودة داخل القائمة المحفوظة
                # ملاحظة: محددات خرائط جوجل قد تتغير ديناميكياً، لذا نبحث عن الروابط التي تؤدي إلى مواقع (place)
                elements = self.driver.find_elements(
                    By.XPATH, "//a[contains(@href, '/maps/place/')]"
                )
                place_urls = [elem.get_attribute("href") for elem in elements]

                if not place_urls:
                    print(arab_txt("[-] لم يتم العثور على روابط مواقع. تأكد من صحة الرابط أو قم بالتمرير يدوياً لأسفل."))
                    return

                print(arab_txt(f"[+] تم العثور على {len(place_urls)} موقع. جاري استخراج الإحداثيات..."))

                # فتح ملف CSV لبدء كتابة البيانات المستخرجة
                with open(
                    output_csv, mode="w", newline="", encoding="utf-8"
                ) as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        ["Location Name", "Latitude", "Longitude"]
                    )  # العناوين الرئيسية

                    for idx, url in enumerate(place_urls, 1):
                        try:
                            self.driver.get(url)
                            # الانتظار حتى يتغير الرابط ويحتوي على الإحداثيات @lat,lng
                            WebDriverWait(self.driver, 15).until(
                                lambda d: "@" in d.current_url
                            )

                            current_url = self.driver.current_url
                            lat, lng = self.extract_coords_from_url(current_url)

                            # استخراج اسم الموقع من عنوان الصفحة (Title) لتفادي تغير الـ Xpath للموقع
                            place_name = self.driver.title.split(" - ")[0]

                            if lat and lng:
                                writer.writerow([place_name, lat, lng])
                                print(arab_txt(
                                    f"[{idx}] تم بنجاح استخراج: {place_name} ({lat}, {lng})"
                                ))
                            else:
                                print(arab_txt(
                                    f"[-] فشل استخراج إحداثيات الموقع رقم {idx} من الرابط."
                                ))

                            time.sleep(2)  # إراحة المتصفح لتجنب الحظر الإلكتروني
                        except Exception as loc_error:
                            print(arab_txt(f"[-] خطأ أثناء معالجة الموقع {idx}: {loc_error}"))

                print(arab_txt(f"[+] اكتملت العملية! تم حفظ البيانات في الملف: {output_csv}"))

            except Exception as e:
                print("i am sulaiman 5")

                print(arab_txt(f"[-] حدث خطأ غير متوقع أثناء الفحص والتحليل: {e}"))
            finally:
                if self.driver:
                    self.driver.quit()


    # =====================================================================
    # المرحلة الثانية: كلاس الحسابات الجغرافية وترتيب المسار (Route Optimization)
    # =====================================================================
    class RouteOptimizer:
        """كلاس مسؤول عن تطبيق المنطق الرياضي لترتيب المحطات جغرافياً من الأقرب فالأقرب."""

        @staticmethod
        def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
            """حساب المسافة بين نقطتين على سطح الأرض باستخدام معادلة Haversine الحسابية."""
            R = 6371.0  # نصف قطر كوكب الأرض بالكيلومترات

            # تحويل الدرجات الجغرافية إلى راديان (Radians)
            phi1, phi2 = math.radians(lat1), math.radians(lat2)
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)

            # تطبيق القانون الرياضي لهيفرسين
            a = (
                math.sin(delta_phi / 2) ** 2
                + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
            )
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            return R * c  # المسافة بالكيلومترات

        def optimize_route(
            self, csv_file: str, current_loc: tuple, final_dest: tuple = None
        ) -> list:
            """قراءة المحطات من الـ CSV وترتيبها بالاعتماد على خوارزمية الجار الأقرب (Nearest Neighbor)."""
            locations = []

            # 1. قراءة البيانات من ملف CSV
            try:
                with open(csv_file, mode="r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        locations.append(
                            {
                                "name": row["Location Name"],
                                "lat": float(row["Latitude"]),
                                "lng": float(row["Longitude"]),
                            }
                        )
            except Exception as e:
                print(arab_txt(f"[-] خطأ أثناء قراءة ملف CSV: {e}"))
                return []

            # 2. منطق الترتيب من الأقرب فالأقرب
            ordered_route = []
            current_lat, current_lng = current_loc

            print(arab_txt("[+] جاري معالجة النقاط وترتيبها حسب الأقرب جغرافياً..."))
            while locations:
                closest_place = None
                min_distance = float("inf")

                # البحث عن النقطة الأقرب للموقع الحالي الحالي
                for place in locations:
                    dist = self.haversine_distance(
                        current_lat, current_lng, place["lat"], place["lng"]
                    )
                    if dist < min_distance:
                        min_distance = dist
                        closest_place = place

                # نقل النقطة الأقرب إلى قائمة المسار المرتب وحذفها من القائمة القديمة
                ordered_route.append(closest_place)
                locations.remove(closest_place)

                # تحديث الموقع الحالي ليصبح هو الموقع الجديد الذي وصلنا إليه
                current_lat, current_lng = closest_place["lat"], closest_place["lng"]

            return ordered_route


    # =====================================================================
    # المرحلة الثالثة: كلاس رسم وبناء المسار (Route Plotting)
    # =====================================================================
    class RoutePlotter:
        """ كلاس يحتوي على خيارين لرسم المسارات: الأتمتة التفاعلية أو التعديل الذكي للرابط URL. """

        def __init__(self, user_data_dir: str = None, profile_dir: str = "Default"):
            self.user_data_dir = user_data_dir
            self.profile_dir = profile_dir

        # def plot_via_ui_automation(self, current_loc_str: str, ordered_route: list):
        #     """ الخيار الأول: أتمتة تفاعلية بالكامل لفتح الخرائط وإضافة المحطات يدوياً (UI Automation)."""
        #     options = Options()
        #     if self.user_data_dir:
        #         options.add_argument(f"--user-data-dir={self.user_data_dir}")
        #         options.add_argument(f"--profile-directory={self.profile_dir}")
        #     options.add_argument("--start-maximized")

        #     service = Service(ChromeDriverManager().install())
        #     driver = webdriver.Chrome(service=service, options=options)

        #     try:
        #         print(arab_txt("[+] جاري فتح صفحة اتجاهات خرائط جوجل التفاعلية..."))
        #         driver.get("https://www.google.com/maps/dir/")
        #         wait = WebDriverWait(driver, 20)

        #         # كتابة الموقع الحالي في الخانة الأولى
        #         # استخدام المحدد المعتمد لخانة الإدخال الأولى في قسم الاتجاهات
        #         start_input = wait.until(
        #             EC.presence_of_element_with_focused_element(
        #                 (By.XPATH, "//div[@id='sb_ifc51']/input")
        #             )
        #         )
        #         # في حال لم يعمل الـ Xpath السابق نتيجة لتحديثات جوجل، نستخدم كلاس البحث العام كاحتياط:
        #         if not start_input:
        #             start_input = driver.find_elements(By.CLASS_CODES, "tactile-searchbox-input")[0]

        #         start_input.send_keys(current_loc_str)
        #         start_input.send_keys(Keys.ENTER)
        #         time.sleep(2)

        #         # إضافة المحطات المرتبة بالتتابع عبر أتمتة زر "Add Stop"
        #         for idx, station in enumerate(ordered_route):
        #             print(arab_txt(f"[+] جاري إضافة المحطة: {station['name']} إلى واجهة الخرائط."))

        #             # الضغط على زر "إضافة وجهة / محطة جديدة"
        #             # نستخدم الـ Xpath النصي المرن أو المحدد الهيكلي لزر إضافة محطة
        #             add_stop_btn = wait.until(
        #                 EC.element_to_be_clickable(
        #                     (By.XPATH, "//span[contains(text(),'إضافة وجهة') or contains(text(),'Add stop')]/..")
        #                 )
        #             )
        #             add_stop_btn.click()
        #             time.sleep(1.5)

        #             # العثور على آخر خانة إدخال تم إنشاؤها للوجهة وكتابة الإحداثيات داخلها لضمان الدقة
        #             inputs = driver.find_elements(
        #                 By.XPATH, "//div[contains(@id, 'sb_ifc')]/input"
        #             )
        #             active_input = inputs[-1]  # الخانة الأخيرة المضافة تظهر أسفل القائمة
        #             active_input.send_keys(f"{station['lat']},{station['lng']}")
        #             active_input.send_keys(Keys.ENTER)
        #             time.sleep(2)

        #         print(arab_txt("[+] تم الانتهاء من بناء المسار تفاعلياً، يمكنك استعراض المتصفح الآن."))
        #         # نترك المتصفح مفتوحاً ليعاين المستخدم المسار
        #         input(arab_txt("[*] اضغط Enter هنا لإنهاء وإغلاق المتصفح تالياً..."))

        #     except Exception as e:
        #         print(arab_txt(f"[-] خطأ أثناء الأتمتة التفاعلية للمسار: {e}"))
        #     finally:
        #         driver.quit()

        def generate_multi_stop_url(self, current_loc: tuple, ordered_route: list) -> str:
            """الخيار الثاني: تركيب وهندسة رابط ذكي ومباشر يحتوي على جميع المحطات دفعة واحدة."""
            print(arab_txt("[+] جاري تركيب وهندسة الرابط الذكي (URL Manipulation)..."))
            base_url = "https://www.google.com/maps/dir/"
            print("i am sulaiman 55")
            # إضافة نقطة البداية للرابط
            url_parts = [f"{current_loc[0]},{current_loc[1]}"]

            # إضافة المحطات المرتبة بالتتابع الرياضي التنازلي
            for station in ordered_route:
                url_parts.append(f"{station['lat']},{station['lng']}")

            # دمج الأجزاء عبر علامة المائل الأمامي '/' ليتشكل الرابط النهائي
            final_url = base_url + "/".join(url_parts)
            print("url_parts",url_parts)
            print("final_url",final_url)
            return final_url

# =================================
# =================================


    # --- إعدادات المستخدم (يجب تعديلها لتتوافق مع جهازك) ---
    # ضع هنا مسار مجلد User Data الخاص بكروم في جهازك (تجد المسار عبر كتابة chrome://version في متصفحك)
    CHROME_USER_DATA = r"C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data\Default"
    GOOGLE_SAVED_LIST_URL = r"https://maps.app.goo.gl/yMYr7c6LAEiWXqVt9"  # Mapes list

    # إحداثيات موقعك الحالي (مثال: مسقط، عمان)
    MY_CURRENT_LAT_LNG = (23.629079, 58.197913)
    MY_CURRENT_ADDRESS_TEXT = "Muscat, Oman"

    CSV_FILE_NAME = r"my_optimized_destinations.csv"

    # -----------------------------------------------------------------
    # تنفيذ المرحلة الأولى: استخراج البيانات وحفظها في الـ CSV
    # -----------------------------------------------------------------
    print(arab_txt("\n--- بدأ تنفيذ المرحلة الأولى: كشط واستخراج البيانات ---"))
    scraper = GoogleMapsScraper(
        user_data_dir=CHROME_USER_DATA, profile_dir="Default"
    )
    # ملاحظة: تم إيقاف الاستدعاء المباشر للمرحلة الأولى بالأسفل حتى لا يعتمد الكود على مسار كروم الخاص بك بشكل إجباري عند الفحص الأول.
    # يمكنك تفعيل السطر التالي بمجرد إدخال مسار الكروم الفعلي الخاص بك:
    scraper.scrape_saved_list(list_url=GOOGLE_SAVED_LIST_URL, output_csv=CSV_FILE_NAME)

    # لأغراض التجربة الفورية إذا لم يتوفر ملف CSV بعد، سنقوم بإنشاء ملف وهمي يحتوي على البيانات:
    with open(CSV_FILE_NAME, mode="w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Location Name", "Latitude", "Longitude"])
        w.writerow(["شركة وصل", 23.575167, 58.398224 ])
        w.writerow(["شركة وصل", 23.557165, 58.401804 ])
        w.writerow(["شركة وصل", 23.588159, 58.357191 ])
        w.writerow(["شركة وصل", 23.659263, 58.182958 ])
        w.writerow(["شركة وصل", 23.599724, 58.157211 ])
        w.writerow(["شركة وصل", 23.590745, 58.243986 ])
        w.writerow(["شركة وصل", 23.589860, 58.132985 ])
        w.writerow(["شركة وصل", 23.675182, 58.136013 ])
        w.writerow(["شركة وصل", 23.627251, 58.140637 ])
        w.writerow(["شركة وصل", 23.617451, 58.193704 ])
        w.writerow(["شركة وصل", 23.578266, 58.299291 ])
        w.writerow(["شركة وصل", 23.593155, 58.448578 ])
        w.writerow(["شركة وصل", 23.588299, 58.372130 ])
        w.writerow(["شركة وصل", 23.592711, 58.444109 ])
        w.writerow(["شركة وصل", 23.682343, 58.189057 ])
        w.writerow(["شركة وصل", 23.591128, 58.404214 ])
        w.writerow(["شركة وصل", 23.596797, 58.428119 ])
        w.writerow(["شركة وصل", 23.592319, 58.451948 ])
        w.writerow(["شركة وصل", 23.595529, 58.439725 ])
        w.writerow(["شركة وصل", 23.583354, 58.424763 ])
        w.writerow(["شركة وصل", 23.586579, 58.370437 ])
        w.writerow(["شركة وصل", 23.588264, 58.444612 ])
        w.writerow(["شركة وصل", 23.589101, 58.387257 ])



    # -----------------------------------------------------------------
    # تنفيذ المرحلة الثانية: ترتيب المحطات بالأقرب (Haversine Logic)
    # -----------------------------------------------------------------
    print(arab_txt("\n--- بدأ تنفيذ المرحلة الثانية: معالجة وترتيب المسار ---"))
    optimizer = RouteOptimizer()
    optimized_stations = optimizer.optimize_route(
        csv_file=CSV_FILE_NAME, current_loc=MY_CURRENT_LAT_LNG
    )

    print(arab_txt("\nنتائج الترتيب الجغرافي الذكي للمحطات:"))
    for i, station in enumerate(optimized_stations, 1):
        print(arab_txt(f"المحطة [{i}]: {station['name']} -> ({station['lat']}, {station['lng']})"))

    # -----------------------------------------------------------------
    # تنفيذ المرحلة الثالثة: رسم المسارات (استعراض الخيارين المتاحين)
    # -----------------------------------------------------------------
    print(arab_txt("\n--- بدأ تنفيذ المرحلة الثالثة: رسم وبناء المسار النهائي ---"))
    plotter = RoutePlotter(user_data_dir=CHROME_USER_DATA, profile_dir="Default")

    # الخيار الثاني أولاً (تعديل الرابط الذكي URL Manipulation): وهو الخيار الأسرع والأنظف برمجياً
    smart_url = plotter.generate_multi_stop_url(
        current_loc=MY_CURRENT_LAT_LNG, ordered_route=optimized_stations
    )
    print(arab_txt(f"\n[+] الرابط الذكي الجاهز للاستخدام المباشر لجميع المحطات:\n{smart_url}\n"))

    # الخيار الأول (الأتمتة التفاعلية لواجهة المستخدم UI Automation):
    # قم بإلغاء التعليق عن السطر أدناه إذا كنت ترغب في رؤية الأداة وهي تضغط وتكتب بنفسها داخل المتصفح:
    # plotter.plot_via_ui_automation(current_loc_str=MY_CURRENT_ADDRESS_TEXT, ordered_route=optimized_stations)


    # 3. توليد الرابط (smart_url)

    smart_urll = smart_url # هذا الرابط الذي ينتجه كودك
    return {"url": smart_urll} # إرسال الرابط للواجهة

# =====================================================================
# منطقة التشغيل الرئيسية وفحص المكونات البرمجية (Execution Block)
# =====================================================================
if __name__ == '__main__':


    app.run(debug=True)

        # <h1>مرحباً بك! أخبرنا عن نفسك</h1>
