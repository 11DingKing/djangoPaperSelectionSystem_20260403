"""
初始化测试数据
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from topics.models import Topic

User = get_user_model()


class Command(BaseCommand):
    help = '初始化测试数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化数据...')
        
        # 创建教师账号
        teachers = [
            {'username': 'teacher1', 'real_name': '张教授', 'teacher_id': 'T001', 'email': 'zhang@example.com'},
            {'username': 'teacher2', 'real_name': '李教授', 'teacher_id': 'T002', 'email': 'li@example.com'},
            {'username': 'teacher3', 'real_name': '王教授', 'teacher_id': 'T003', 'email': 'wang@example.com'},
        ]
        
        created_teachers = []
        for t in teachers:
            user, created = User.objects.get_or_create(
                username=t['username'],
                defaults={
                    'real_name': t['real_name'],
                    'role': User.Role.TEACHER,
                    'teacher_id': t['teacher_id'],
                    'email': t['email'],
                }
            )
            if created:
                user.set_password('123456')
                user.save()
                self.stdout.write(f'  创建教师: {user.real_name}')
            created_teachers.append(user)
        
        # 创建学生账号
        students = [
            {'username': 'student1', 'real_name': '陈同学', 'student_id': '2024001'},
            {'username': 'student2', 'real_name': '刘同学', 'student_id': '2024002'},
            {'username': 'student3', 'real_name': '赵同学', 'student_id': '2024003'},
            {'username': 'student4', 'real_name': '孙同学', 'student_id': '2024004'},
            {'username': 'student5', 'real_name': '周同学', 'student_id': '2024005'},
        ]
        
        for s in students:
            user, created = User.objects.get_or_create(
                username=s['username'],
                defaults={
                    'real_name': s['real_name'],
                    'role': User.Role.STUDENT,
                    'student_id': s['student_id'],
                }
            )
            if created:
                user.set_password('123456')
                user.save()
                self.stdout.write(f'  创建学生: {user.real_name}')
        
        # 创建论文题目
        topics_data = [
            {
                'teacher': created_teachers[0],
                'title': '基于深度学习的图像识别系统研究',
                'description': '''本课题旨在研究基于深度学习技术的图像识别系统。

主要研究内容：
1. 深度学习模型的选择与优化
2. 图像预处理与数据增强技术
3. 模型训练与调参策略
4. 系统性能评估与优化

预期成果：
- 完成一个可用的图像识别系统原型
- 撰写相关技术文档和论文''',
                'requirements': '要求学生具备Python编程基础，了解机器学习基本概念，有一定的数学基础。',
                'max_students': 2,
            },
            {
                'teacher': created_teachers[0],
                'title': '智能推荐算法的研究与实现',
                'description': '''研究基于协同过滤和内容推荐的混合推荐算法。

研究方向：
1. 用户行为分析与建模
2. 协同过滤算法优化
3. 冷启动问题解决方案
4. 推荐系统评估指标

应用场景：电商平台、视频网站、新闻资讯等。''',
                'requirements': '熟悉Python或Java，了解数据库操作，有数据分析经验者优先。',
                'max_students': 1,
            },
            {
                'teacher': created_teachers[1],
                'title': 'Web应用安全漏洞检测工具开发',
                'description': '''开发一款自动化的Web应用安全漏洞检测工具。

功能需求：
1. SQL注入漏洞检测
2. XSS跨站脚本攻击检测
3. CSRF漏洞检测
4. 生成安全检测报告

技术栈：Python + Flask/Django''',
                'requirements': '熟悉Web开发技术，了解常见Web安全漏洞原理，有网络安全兴趣。',
                'max_students': 2,
            },
            {
                'teacher': created_teachers[1],
                'title': '基于微服务架构的在线教育平台设计',
                'description': '''设计并实现一个基于微服务架构的在线教育平台。

系统模块：
1. 用户服务（注册、登录、权限管理）
2. 课程服务（课程管理、视频播放）
3. 订单服务（购买、支付）
4. 评论服务（课程评价、互动）

技术要求：Spring Cloud / Docker / Kubernetes''',
                'requirements': '熟悉Java开发，了解微服务架构，有分布式系统开发经验者优先。',
                'max_students': 3,
            },
            {
                'teacher': created_teachers[2],
                'title': '移动端健康管理APP开发',
                'description': '''开发一款面向个人用户的健康管理移动应用。

核心功能：
1. 健康数据记录（体重、血压、运动等）
2. 数据可视化展示
3. 健康建议推送
4. 社交分享功能

支持平台：Android / iOS（可选其一）''',
                'requirements': '熟悉移动端开发（Android/iOS/Flutter），有UI设计意识。',
                'max_students': 2,
            },
            {
                'teacher': created_teachers[2],
                'title': '区块链技术在供应链管理中的应用研究',
                'description': '''研究区块链技术在供应链管理领域的应用场景和实现方案。

研究内容：
1. 区块链基础技术研究
2. 供应链溯源系统设计
3. 智能合约开发
4. 系统原型实现

技术方向：Hyperledger Fabric / Ethereum''',
                'requirements': '了解区块链基本原理，熟悉至少一门编程语言，有较强的学习能力。',
                'max_students': 1,
            },
        ]
        
        for t in topics_data:
            topic, created = Topic.objects.get_or_create(
                title=t['title'],
                teacher=t['teacher'],
                defaults={
                    'description': t['description'],
                    'requirements': t['requirements'],
                    'max_students': t['max_students'],
                }
            )
            if created:
                self.stdout.write(f'  创建题目: {topic.title}')
        
        # 创建管理员
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'real_name': '系统管理员',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write('  创建管理员: admin')
        
        self.stdout.write(self.style.SUCCESS('数据初始化完成！'))
        self.stdout.write('')
        self.stdout.write('测试账号:')
        self.stdout.write('  教师: teacher1 / 123456')
        self.stdout.write('  学生: student1 / 123456')
        self.stdout.write('  管理员: admin / admin123')
