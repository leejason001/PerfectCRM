#coding:utf-8
from django.db import models
from django.contrib.auth.models import  User

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.



class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):#To command: python manage.py createsuperuser
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)#存从命令行输入的用户名、密码
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64,verbose_name="realName")
    role = models.ManyToManyField( "Role", blank=True, null=True )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField( default=True )
    #is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def get_short_name(self):
        return "alex"

    class Meta:
        permissions = (
            ("crm_table_list", "可以允许是正文搞自己"),
            ("crm_table_view", "可以查看表中所有数据"),
            ("crm_table_list_view", "可以访问表里每条数据的修改页"),
            ("crm_table_list_change", "修改修改"),
            ("crm_table_obj_add_view", "可以访问数据增加页"),
            ("crm_table_obj_add", "可以创建表里的数据"),
        )

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin


# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#
#
#
#
#     def __str__(self): #__unicode__
#         return self.name

class Role(models.Model):

    name = models.CharField(max_length=64,unique=True)
    menu = models.ManyToManyField('Menus', blank=True)
    def __str__(self):
        return self.name


class CustomerInfo(models.Model):

    name = models.CharField(max_length=64,default=None)
    contact_type_choices = ((0,'qq'),(1,'weixin'),(2,'phone'))
    contact_type = models.SmallIntegerField(choices=contact_type_choices,default=0)
    contact = models.CharField(max_length=64,unique=True)
    source_choices = ((0,'QQ'),
                      (1,'51CTO'),
                      (2,'baidu'),
                      (3,'zhiHu'),
                      (4,'Referral'),
                      (5,'Others'),
                      )
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.ForeignKey("self",blank=True,null=True,verbose_name="Referral")
    consult_courses = models.ManyToManyField("Course",verbose_name="consult_courses")
    consult_content = models.TextField(verbose_name="consult_content")
    status_choices = ((0,'no sign up'),(1,'has signed up'),(2,'has quited'))
    status = models.SmallIntegerField(choices=status_choices)
    consultant = models.ForeignKey("UserProfile",verbose_name="courseConsultant")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Student(models.Model):

    customer = models.OneToOneField("CustomerInfo")
    class_grades = models.ManyToManyField("ClassList")

    def __str__(self):
        return "%s"%self.customer


class CustomerFollowUp(models.Model):

    customer = models.ForeignKey("CustomerInfo")
    content = models.TextField(verbose_name="content")
    user = models.ForeignKey("UserProfile",verbose_name="employeeFollowing")
    status_choices  = ((0,'noPays'),
                       (1,'Pay in a month'),
                       (2,'Pay in 2 weeks'),
                       (3,'Payed'),
                       )
    status = models.SmallIntegerField(choices=status_choices)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content


class Course(models.Model):

    name = models.CharField(verbose_name='courseName',max_length=64,unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="period(month)",default=5)
    outline = models.TextField(verbose_name="outline")

    def __str__(self):
        return self.name


class ClassList(models.Model):

    branch = models.ForeignKey("Branch")
    course = models.ForeignKey("Course")
    class_type_choices = ((0,'allIn'),(1,'weekEnd'),(2,'onLine'))
    class_type = models.SmallIntegerField(choices=class_type_choices,default=0)
    semester = models.SmallIntegerField(verbose_name="semester")
    teachers = models.ManyToManyField("UserProfile",verbose_name="teacher")
    start_date = models.DateField("start_date")
    graduate_date = models.DateField("graduate_date",blank=True,null=True)
    contract_template = models.ForeignKey("ContractTemplate",null=True, blank=True)
    def __str__(self):

        return "%s(%s)" %(self.course.name,self.semester)

    class Meta:
        unique_together =  ('branch','class_type','course','semester')


class CourseRecord(models.Model):

    class_grade = models.ForeignKey("ClassList",verbose_name="class_grade")
    day_num = models.PositiveSmallIntegerField(verbose_name="day_num")
    teacher = models.ForeignKey("UserProfile")
    title = models.CharField("title",max_length=64)
    content = models.TextField("content")
    has_homework = models.BooleanField("has_homework",default=True)
    homework = models.TextField("homeworkCaption",blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  "%s(%s)" %(self.class_grade,self.day_num)

    class Meta:
        unique_together = ('class_grade','day_num')



class StudyRecord(models.Model):

    course_record = models.ForeignKey("CourseRecord")
    student = models.ForeignKey("Student")

    score_choices = ((100,"A+"),
                     (90,"A"),
                     (85,"B+"),
                     (80,"B"),
                     (75,"B-"),
                     (70,"C+"),
                     (60,"C"),
                     (40,"C-"),
                     (-50,"D"),
                     (0,"N/A"), #not avaliable
                     (-100,"COPY"), #not avaliable
                     )
    score = models.SmallIntegerField(choices=score_choices,default=0)
    show_choices = ((0,'absence'),
                    (1,'signed'),
                    (2,'late'),
                    (3,'leaveEarly'),
                    )
    show_status = models.SmallIntegerField(choices=show_choices,default=1)
    note = models.TextField("note",blank=True,null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return "%s %s %s" %(self.course_record,self.student,self.score)

class Branch(models.Model):
    name = models.CharField(max_length=64,unique=True)
    addr = models.CharField(max_length=128,blank=True,null=True)
    def __str__(self):
        return self.name

class Menus(models.Model):
    name = models.CharField(max_length=64)
    url_type_choices = ((0, 'absolute'),(1, 'dynamic'))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            ('name', 'url_name'),
        )

class ContractTemplate(models.Model):
    name = models.CharField(max_length=64)
    content = models.TextField()
    date    = models.DateField(auto_now_add=True)


class StudentEnrollment(models.Model):
    customer = models.ForeignKey("CustomerInfo")
    class_grade = models.ForeignKey("ClassList")
    consultant = models.ForeignKey("UserProfile")
    contract_agreed = models.BooleanField(default=False)
    contract_signed_date = models.DateTimeField(null=True, blank=True)
    contract_approved = models.BooleanField(default=False)
    contract_approved_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("customer", "class_grade")
    def __str__(self):
        return "%s"%self.customer

class PaymentRecord(models.Model):
    enrollment = models.ForeignKey("StudentEnrollment")
    payment_type_choices = ((0, 'BaoMingFei'), (1, 'XueFei'), (2, 'TuiFei'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices, default=0)
    amount = models.IntegerField('FeiYong', default=500)
    payee      = models.ForeignKey("UserProfile")
    date       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s"%self.enrollment
