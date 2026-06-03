#  اليوم انتهيت من فهم الجت بعدما كان صندوق اسود 
# الجت مهم جدا بالنسبه لكل مبرمج لحفظ التعديلات و الرجوع للتعديلات القديمة و العمل الجماعي
# اذا كنت تشبهني اختصر الحياة و اطلع على ملخصي


""" المستوى 1: أساسيات Git (لازم قبل GitHub)
تثبيت Git على جهازك
فهم كلمات Git الأساسية:
repository
commit
stage / staging area
branch
إنشاء مشروع Git جديد
إضافة ملفات
عمل أول commit
فهم حالة الملفات:
untracked
staged
modified
"""

""" المستوى 2: العمل الاحترافي بـ Git
استخدام الفروع (branches)
الدمج (merge)
حلّ تعارضات الدمج (merge conflicts)
إعادة كتابة التاريخ (reset / revert)
تجاهل ملفات (gitignore)
"""

""" المستوى 3: أساسيات GitHub
إنشاء حساب GitHub
رفع مشروع من جهازك إلى GitHub
استنساخ مشروع clone
push / pull
إنشاء مستودع جديد
إدارة المفاتيح (SSH Key)
"""

""" المستوى 4: احتراف GitHub
الـ Pull Request
الـ Issues
GitHub Projects
GitHub Actions
التعاون بين فرق العمل
حماية الفروع Branch Protection
الـ Fork
"""


""" كلمات Git الأساسية:
repository           ذاكرة المشروع
Working Directory    المجلد العادي اللي فيه ملفاتك
Staging Area         المكان الي تنظاف فيه الملفات الي نرد نحفظها git add لما نعمل
commit               الحفظ الرسمي
staging area branch  وتقدر تسوي فرع جديد باسم للتعديل بدون لمس النسخة الأصلية
untracked            شايفها… لكنها مو مضافة Git ملفات في المجلد
modified             commit للملف و باقي تعمل git add يعني عملت 
committed            يعني: تم حفظ الملف رسميًا
"""
# ==============================================================================



# ==============================================================================

# -------------------------------- Git اعدادات ---------------------------------

# vs code يشتغل في Git التأكد إن
# git --version

# انشاء مستودع
# git init

# اظهار الملفات الموجودة الغير مضافة
# git status

# من أنت لتسجل اسمك وبريدك في تاريخ المشروع Git لنعرف
# git config --global user.name "Hamid"
# git config --global user.email "alalbah@gmail.com"

# أضافة التعديلات و الملفات
# git add hello.txt login.py
# أو
# git add .

# اذا تريد تنتقل فرع ثاني بس ما تريد ترفع الملفات بعدك احفظ التعديلات مؤقتا
# git stash
# بعد ما ترجع اعمل
# git stash pop

# الحفظ الرسمي Commit عمل 
# رسالة تشرح نوع التغيير message اختصار لكلمة  = -m
# git commit -m "My first commit"

# اللي سويتها أثناء العمل commits كيف تشوف قائمة كل الـ
# git log            كل التفاصيل
# git log --oneline  مختصر 

#  لتشوف أسماء الملفات اللي تغيّرت 
# اسم الملفات و كم سطر تغيّر
# git log --stat

# شوف الفروع الموجودة فيه
# git branch

# إنشاء فرع جديد
# git branch feature-login

# للتنقل بين الفروع
# تلاحض كل فرع عنده نفس الملفات لاكن اكوادها مختلفة حسب التعديل
# git switch main    

# نفّذ الدمج
# لازم تقف على الفرع الي تريده يتعدل
# ملاحظة اذا دمجت و فرع ثاني اراد يدمج و هو معدل نفس الاسطر الي انت عدلتهن راح يظهر تنبيه و يحتاج تختاروا بشكل يدوي
# git merge feature-login

# كيف أرجع لنسخة قديمة
# git log --oneline
# commit رقم الـ
# git checkout ba87665
# او
# git switch --detach ba87665

# القديم commitطرق الرجوع للـ
# -- git reset --
# و التعديلات و يقف على المختار commit يحذف الـ
# git reset --hard B
# commit يبقى تعمل git add و يحتفظ بالتعديلات كنك عامل commitيحذف الـ
# git reset --soft HEAD~1
# ولا يحذف التعديلات من الملف git add و الـ commit يحذف الـ
# git reset --mixed HEAD~1 أو git reset HEAD~1
# -- git revert --
# المختار commit جديدًا من الـ commit بل ينشئ commit لا يحذف الـ 
# git revert C

# يمكن استرجاعه باستخدام reset باستخدام commit إذا حذفت
# git reflog
# ID ثم بالـ
# git reset --hard f6a7594  
# التعديلات ما ترجع اذا عملت 
# git reset f6a7594  


# commit إذا أردت تتصفح النسخة القديمة في
# git checkout ba87665
# Git الحديث
# git switch --detach ba87665

# commit عرض التغييرات قبل عمل 
# git diff

# لحذف ملف من الفرع
# git rm test.py
# git commit -m "Remove test.py"

# لحذف فرع
# التي تم دمجها في فرع آخر commits طبعا حذف الفرع لا يعني حذف الـ
# git branch -d branch-name
# branch is not fully merged لم يتم دمجها commits اذا ظهرت رسالة يعني يوجد 
# إذا كنت متأكدًا أنك تريد حذف بكل الاحوال
# git branch -D branch-name

# -------------------------------- GitHup مع Git اعدادات ربط ---------------------------------

# -- اعدادات ربط --

# vs code اكتب في
# يعرض المجلد الحالي الذي تعمل بداخله
# pwd

# GitHup ربط المشروع الحالي بمستودع
# مثل GitHupالرابط الي اعطاك اياه الـ
# git remote add origin https://github.com/s1j2b1/Git_learn.git
# GitHup اذا اردت ربط الملف الحالي بمستودع مختلف في
# https://github.com/s1j2b1/Git_learn.git
# origin: اختصار بدل يكتب الرابط كامل GitHup تعني المستودع على 

# للتأكد باي مستودع مربوط
# git remote -v

# للتأكد مما سيرفع
# git log --oneline origin/main..HEAD

# رفع المشروع لأول مرة
# git push -u origin main
# المرات القادمة يكفي
# git push أو git push origin main

# جلب التحديثات و دمجها في كودك
# git pull --rebase origin main

# جلب التحديثات دون دمجها
# git fetch
# ثم لرؤية ما هي التحديثات
# git diff HEAD origin/main
# وليست عندك GitHub باللون الأخضر: السطور الجديدة المضافة على 
# باللون الأحمر: السطور التي تم حذفها أو تعديلها أونلاين

# اذا فقط تريد معرفة ما هي أسماء الملفات التي تم تعديلها
# git diff HEAD origin/main --name-status

# لدمج التغييرات اذا اعجبتك
# git merge origin/main

# اذا حصلة مشكلة اثناء جلب البيانات إلغاء عملية الدمج العالقة
# git merge --abort

# GitHub كيف أعرف إذا كنت متأخرًا عن 
# git status
# Your branch is behind 'origin/main' by 2 commits
# GitHub إذا كنت متقدمًا على 
# Your branch is ahead of 'origin/main' by 19 commits


# -- Pull Request (PR) --
# معناها أريد دمج هذا الفرع داخل فرع آخر، هل توافقون؟ GitHub ميزة في 
# تبدأ العمل مع فريق PR مع
# لاكن قبل الدمج يراجع شخص الكود ويوافق أو يطلب تعديلات GitHub فائدته من فرعك ترسل للـ
# مراجعة الكود (Code Review) \ مناقشة التغييرات \ اختبارات تلقائية \ موافقات الفريق

# PR عمل أول
# انتقل إلى الفرع مثلا
# git switch feature-login

# ..أنشئ ملفًا جديدًا مثلا و اكتب فيه
# github_pr.txt

# احفظ التعديل
# git add github_pr.txt
# git commit -m "Add PR example"

# GitHub رفع الفرع إلى 
# git push -u origin feature-login

# التكملة مسؤولية قسم الادارة
# GitHub من المستودع على 

# سيظهر شريط أصفر أو أخضر فيه
# Compare & pull request
# ثم 
# Create Pull Request
# ثم 
# Merge Pull Request
# ثم
# Confirm Merge
# بعدها اذا انتهت مهمة الفرع
# Delete branch

# لما تتعارض الاكواد نعمل استدعاء بيانات الفرع الرئيسي في فرعنا و نحل التعارض 
# git pull origin main
# ثم نعيد الرفع
# git push


# -- Clone --
# وتريد تنزيله كاملًا إلى جهازك GitHub الفكرة عندما ترى مشروعًا على 
# (URL HTTPS رابط المستودع) بدل أن تنشئ مجلدًا وتنسخ الملفات يدويًا، تعمل

# vs code terminal
# cd C:\Users\Lenovo\Desktop\New_folder

# git clone URL
# افتح المشروع
# cd ..

# العمل في الشركات
# Clone = أول مرة
# Pull = كل مرة بعدها


# -- Fork --
#  يستخدم لمشاريع مفتوحة المصدر 
# مباشر إلى المستودع الرئيسي Push او شركات حتى الموظفون أنفسهم لا يملكون
# يؤثر عليك شخصيًا بدل أن تنتظر أشهرًا حتى يصلحه أحد Bug أو أنت وجدت
# تمكنك تملك نسخة من مشروع الشركة مربوطة بالشركة و اي تحديث ممكن تطلع ليه
# Fork الكود اضغط github من 
# tensorflow/tensorflow -> s1j2b1/tensorflow
# ثم 
# git clone https://github.com/s1j2b1/tensorflow.git

# لما يصير تحديث
# tensorflow/tensorflow    ← أحدث
# s1j2b1/tensorflow        ← أقدم
# لذلك تربط مشروعك المحلي بمصدرين

# الجديدة إلى نسختك TensorFlow تدخل تحديثات
# git fetch upstream
# ثم
# git merge upstream/main أو git rebase upstream/main

# في أي مشروع مفتوح المصدر ستجد
# Issues
# الآخرين Pull Requests مراجعة  , طرح سؤال تقني , Feature اقتراح , Bug يمكنك: الإبلاغ عن 
# Issue هل أحد أبلغ عن المشكلة؟ إذا لا أنشئ









# -------------------------------------------------------------------


# الإعداد الأولي (مرة واحدة فقط)
# من أنت GitHub قبل أن ترفع، يجب أن يعرف
# git config --global user.name "sulaiman"
# git config --global user.email "s1j2b1@gmail.com"

# أنشئ نيو هستري على الجت هب بيعطيك هذلا الكودات لربط الجت هب مع التيرمنل

# اذا كان الهستري ما يزال فارغ
# …or create a new repository on the command line

# اذا رفعت ملفات على هذا الهستري قبل
# …or push an existing repository from the command line


# -----------------------------
# هذه هي "الخطة" التي ستكررها كلما أجريت تعديلاً:

# قبل أن ترفع أي شيء ليظهر قائمة بالملفات التي عدلتها ولم ترفعها بعد
# git status.

# التجهيز (Stage):
# git add .

# التثبيت (Commit): سجل التعديلات مع وصف (رسالة)
# git commit -m "تحديث واجهة لوحة التحكم وتحسين خوارزمية التنبؤ"

# الرفع اول مرة (Push):
# git push -u origin main
# المرات القادمة فقط تحديث
# git push


# --------------------------- ملاحظات ---------------------------
# لرفع ملف محدد:
# git add file1 name.py file2 name.py


# لرفع كل الملفات (عدا المستثناة): النقطة تعني كل شيء في هذا المجلد
# git add .


# كيف تستثني ملفات لا تريد رفعها؟ (ملفات خاصة!)
# .gitignore أنشئ ملفاً في مجلد المشروع اسمه 







