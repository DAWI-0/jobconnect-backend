from decimal import Decimal
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import CandidateProfile, RecruiterProfile
from apps.companies.models import Company
from apps.jobs.models import Skill, JobOffer
from apps.applications.models import Application
from apps.favorites.models import FavoriteJob
from apps.messaging.models import Conversation, Message
from apps.notifications.models import Notification


User = get_user_model()


class Command(BaseCommand):
    help = "Vide la base de donnees et cree des donnees de demonstration JobConnect."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Supprime les anciennes donnees avant de creer les nouvelles.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        clear = options["clear"]

        # =========================================================
        # CLEAR DATABASE
        # =========================================================

        if clear:
            self.stdout.write(
                self.style.WARNING(
                    "Suppression des anciennes donnees..."
                )
            )

            # Messages
            Message.objects.all().delete()

            # Conversations
            Conversation.objects.all().delete()

            # Notifications
            Notification.objects.all().delete()

            # Applications
            Application.objects.all().delete()

            # Favorites
            FavoriteJob.objects.all().delete()

            # Job offers
            JobOffer.objects.all().delete()

            # Skills
            Skill.objects.all().delete()

            # Recruiter profiles
            RecruiterProfile.objects.all().delete()

            # Candidate profiles
            CandidateProfile.objects.all().delete()

            # Companies
            Company.objects.all().delete()

            # Users
            User.objects.all().delete()

            self.stdout.write(
                self.style.SUCCESS(
                    "Anciennes donnees supprimees."
                )
            )

        # =========================================================
        # PASSWORDS
        # =========================================================

        ADMIN_PASSWORD = "Admin123!"
        RECRUITER_PASSWORD = "Recruiter123!"
        CANDIDATE_PASSWORD = "Candidate123!"

        # =========================================================
        # ADMIN
        # =========================================================

        admin = User.objects.create_user(
            email="admin@jobconnect.com",
            username="admin",
            first_name="Admin",
            last_name="JobConnect",
            password=ADMIN_PASSWORD,
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Admin cree : admin@jobconnect.com"
            )
        )

        # =========================================================
        # RECRUITER USERS
        # =========================================================

        recruiter1 = User.objects.create_user(
            email="recruiter1@jobconnect.com",
            username="recruiter1",
            first_name="Yassine",
            last_name="Alaoui",
            password=RECRUITER_PASSWORD,
            role=User.Role.RECRUITER,
            is_active=True,
        )

        recruiter2 = User.objects.create_user(
            email="recruiter2@jobconnect.com",
            username="recruiter2",
            first_name="Sara",
            last_name="Bennani",
            password=RECRUITER_PASSWORD,
            role=User.Role.RECRUITER,
            is_active=True,
        )

        recruiter3 = User.objects.create_user(
            email="recruiter3@jobconnect.com",
            username="recruiter3",
            first_name="Omar",
            last_name="Amrani",
            password=RECRUITER_PASSWORD,
            role=User.Role.RECRUITER,
            is_active=True,
        )

        # =========================================================
        # CANDIDATE USERS
        # =========================================================

        candidate1 = User.objects.create_user(
            email="candidate1@jobconnect.com",
            username="candidate1",
            first_name="Mohamed",
            last_name="Yassine",
            password=CANDIDATE_PASSWORD,
            role=User.Role.CANDIDATE,
            is_active=True,
        )

        candidate2 = User.objects.create_user(
            email="candidate2@jobconnect.com",
            username="candidate2",
            first_name="Aya",
            last_name="El Idrissi",
            password=CANDIDATE_PASSWORD,
            role=User.Role.CANDIDATE,
            is_active=True,
        )

        # =========================================================
        # COMPANIES
        # =========================================================

        company1 = Company.objects.create(
            name="TechNova Morocco",
            description=(
                "Entreprise marocaine specialisee dans le developpement "
                "de solutions digitales et logiciels innovants."
            ),
            website="https://www.technova.ma",
            email="contact@technova.ma",
            phone="+212 5 22 10 20 30",
            location="Casablanca, Maroc",
            owner=recruiter1,
            is_active=True,
        )

        company2 = Company.objects.create(
            name="DevSolutions Maroc",
            description=(
                "Societe specialisee dans les applications web, "
                "les APIs et les solutions backend."
            ),
            website="https://www.devsolutions.ma",
            email="contact@devsolutions.ma",
            phone="+212 5 22 30 40 50",
            location="Rabat, Maroc",
            owner=recruiter2,
            is_active=True,
        )

        company3 = Company.objects.create(
            name="Maroc Digital",
            description=(
                "Entreprise digitale qui accompagne les organisations "
                "dans leur transformation numerique."
            ),
            website="https://www.marocdigital.ma",
            email="contact@marocdigital.ma",
            phone="+212 5 24 50 60 70",
            location="Marrakech, Maroc",
            owner=recruiter3,
            is_active=True,
        )

        # =========================================================
        # RECRUITER PROFILES
        #
        # IMPORTANT:
        # Les profils sont deja crees automatiquement par
        # apps/accounts/signals.py lors de la creation du User.
        # On les recupere puis on les complete.
        # =========================================================

        recruiter_profile1 = RecruiterProfile.objects.get(
            user=recruiter1
        )

        recruiter_profile1.company = company1
        recruiter_profile1.phone = "+212 6 10 20 30 40"
        recruiter_profile1.job_title = "Responsable RH"
        recruiter_profile1.save()

        recruiter_profile2 = RecruiterProfile.objects.get(
            user=recruiter2
        )

        recruiter_profile2.company = company2
        recruiter_profile2.phone = "+212 6 20 30 40 50"
        recruiter_profile2.job_title = "IT Recruitment Manager"
        recruiter_profile2.save()

        recruiter_profile3 = RecruiterProfile.objects.get(
            user=recruiter3
        )

        recruiter_profile3.company = company3
        recruiter_profile3.phone = "+212 6 30 40 50 60"
        recruiter_profile3.job_title = "Talent Acquisition Manager"
        recruiter_profile3.save()

        # =========================================================
        # CANDIDATE PROFILES
        #
        # IMPORTANT:
        # Les profils sont deja crees automatiquement par
        # apps/accounts/signals.py.
        # =========================================================

        candidate_profile1 = CandidateProfile.objects.get(
            user=candidate1
        )

        candidate_profile1.phone = "+212 6 61 11 22 33"
        candidate_profile1.location = "Casablanca, Maroc"
        candidate_profile1.bio = (
            "Etudiant ingenieur passionne par le developpement web, "
            "les applications modernes et les technologies backend."
        )
        candidate_profile1.linkedin_url = (
            "https://www.linkedin.com/in/candidate1"
        )
        candidate_profile1.github_url = (
            "https://github.com/candidate1"
        )
        candidate_profile1.save()

        candidate_profile2 = CandidateProfile.objects.get(
            user=candidate2
        )

        candidate_profile2.phone = "+212 6 62 22 33 44"
        candidate_profile2.location = "Rabat, Maroc"
        candidate_profile2.bio = (
            "Developpeuse junior passionnee par React, JavaScript "
            "et la creation d'interfaces web modernes."
        )
        candidate_profile2.linkedin_url = (
            "https://www.linkedin.com/in/candidate2"
        )
        candidate_profile2.github_url = (
            "https://github.com/candidate2"
        )
        candidate_profile2.save()

        # =========================================================
        # SKILLS
        # =========================================================

        skill_names = [
            "Python",
            "Django",
            "Django REST Framework",
            "React",
            "JavaScript",
            "TypeScript",
            "PostgreSQL",
            "Git",
            "Docker",
            "HTML/CSS",
            "Node.js",
            "REST API",
        ]

        skills = {}

        for name in skill_names:
            skill = Skill.objects.create(name=name)
            skills[name] = skill

        # =========================================================
        # JOB 1 - RECRUITER 1
        # =========================================================

        now = timezone.now()

        job1 = JobOffer.objects.create(
            company=company1,
            recruiter=recruiter_profile1,
            title="Developpeur Full Stack",
            description=(
                "Nous recherchons un developpeur Full Stack pour "
                "participer au developpement de nos applications web. "
                "Le candidat travaillera sur le frontend et le backend."
            ),
            location="Casablanca, Maroc",
            contract_type=JobOffer.ContractType.CDI,
            experience_level=JobOffer.ExperienceLevel.JUNIOR,
            salary_min=Decimal("9000.00"),
            salary_max=Decimal("13000.00"),
            remote=True,
            status=JobOffer.Status.PUBLISHED,
            published_at=now,
            deadline=now + timedelta(days=30),
        )

        job1.skills.set(
            [
                skills["Python"],
                skills["Django"],
                skills["React"],
                skills["PostgreSQL"],
                skills["Git"],
            ]
        )

        # =========================================================
        # JOB 2 - RECRUITER 2
        # =========================================================

        job2 = JobOffer.objects.create(
            company=company2,
            recruiter=recruiter_profile2,
            title="Developpeur Backend Django",
            description=(
                "Nous recherchons un developpeur Backend specialise "
                "en Python et Django pour developper des APIs REST "
                "performantes et securisees."
            ),
            location="Rabat, Maroc",
            contract_type=JobOffer.ContractType.CDI,
            experience_level=JobOffer.ExperienceLevel.JUNIOR,
            salary_min=Decimal("8500.00"),
            salary_max=Decimal("12000.00"),
            remote=False,
            status=JobOffer.Status.PUBLISHED,
            published_at=now,
            deadline=now + timedelta(days=25),
        )

        job2.skills.set(
            [
                skills["Python"],
                skills["Django"],
                skills["Django REST Framework"],
                skills["PostgreSQL"],
                skills["Docker"],
            ]
        )

        # =========================================================
        # JOB 3 - RECRUITER 3
        # =========================================================

        job3 = JobOffer.objects.create(
            company=company3,
            recruiter=recruiter_profile3,
            title="Developpeur Frontend React",
            description=(
                "Nous recherchons un developpeur Frontend pour "
                "concevoir des interfaces web modernes, responsives "
                "et performantes avec React."
            ),
            location="Marrakech, Maroc",
            contract_type=JobOffer.ContractType.INTERNSHIP,
            experience_level=JobOffer.ExperienceLevel.ENTRY,
            salary_min=Decimal("4000.00"),
            salary_max=Decimal("6000.00"),
            remote=True,
            status=JobOffer.Status.PUBLISHED,
            published_at=now,
            deadline=now + timedelta(days=20),
        )

        job3.skills.set(
            [
                skills["React"],
                skills["JavaScript"],
                skills["TypeScript"],
                skills["HTML/CSS"],
                skills["Git"],
            ]
        )

        # =========================================================
        # APPLICATION 1
        # CANDIDATE 1 -> JOB 1
        # =========================================================

        application1 = Application.objects.create(
            job_offer=job1,
            candidate=candidate_profile1,
            cover_letter=(
                "Je suis tres interesse par cette opportunite. "
                "Mes competences en Python, Django et React "
                "correspondent aux exigences du poste."
            ),
            status=Application.Status.ACCEPTED,
            recruiter_note=(
                "Profil tres interessant. "
                "Candidature acceptee."
            ),
        )

        # =========================================================
        # APPLICATION 2
        # CANDIDATE 1 -> JOB 2
        # =========================================================

        application2 = Application.objects.create(
            job_offer=job2,
            candidate=candidate_profile1,
            cover_letter=(
                "Je souhaite rejoindre votre equipe backend. "
                "J'ai une bonne experience avec Django, DRF "
                "et PostgreSQL."
            ),
            status=Application.Status.INTERVIEW,
            recruiter_note=(
                "Profil retenu pour un entretien technique."
            ),
        )

        # =========================================================
        # APPLICATION 3
        # CANDIDATE 2 -> JOB 2
        # =========================================================

        application3 = Application.objects.create(
            job_offer=job2,
            candidate=candidate_profile2,
            cover_letter=(
                "Je suis interessee par ce poste et souhaite "
                "developper mes competences dans le backend "
                "et les APIs REST."
            ),
            status=Application.Status.REVIEWING,
            recruiter_note=(
                "Candidature en cours d'etude."
            ),
        )

        # =========================================================
        # APPLICATION 4
        # CANDIDATE 2 -> JOB 3
        # =========================================================

        application4 = Application.objects.create(
            job_offer=job3,
            candidate=candidate_profile2,
            cover_letter=(
                "Le poste correspond parfaitement a mon interet "
                "pour React et le developpement frontend."
            ),
            status=Application.Status.PENDING,
            recruiter_note="",
        )

        # =========================================================
        # FAVORITES
        # =========================================================

        FavoriteJob.objects.create(
            candidate=candidate_profile1,
            job_offer=job3,
        )

        FavoriteJob.objects.create(
            candidate=candidate_profile2,
            job_offer=job1,
        )

        # =========================================================
        # CONVERSATIONS
        # =========================================================

        conversation1 = Conversation.objects.create(
            candidate=candidate_profile1,
            recruiter=recruiter_profile1,
        )

        conversation2 = Conversation.objects.create(
            candidate=candidate_profile2,
            recruiter=recruiter_profile2,
        )

        # =========================================================
        # MESSAGES - CONVERSATION 1
        # =========================================================

        Message.objects.create(
            conversation=conversation1,
            sender=candidate1,
            content=(
                "Bonjour, je souhaite avoir plus d'informations "
                "concernant ma candidature."
            ),
            is_read=True,
        )

        Message.objects.create(
            conversation=conversation1,
            sender=recruiter1,
            content=(
                "Bonjour Mohamed, votre candidature nous interesse. "
                "Nous allons vous contacter prochainement."
            ),
            is_read=True,
        )

        Message.objects.create(
            conversation=conversation1,
            sender=candidate1,
            content=(
                "Merci beaucoup. Je reste disponible pour un entretien."
            ),
            is_read=False,
        )

        # =========================================================
        # MESSAGES - CONVERSATION 2
        # =========================================================

        Message.objects.create(
            conversation=conversation2,
            sender=candidate2,
            content=(
                "Bonjour, je voudrais savoir si ma candidature "
                "est toujours en cours d'etude."
            ),
            is_read=True,
        )

        Message.objects.create(
            conversation=conversation2,
            sender=recruiter2,
            content=(
                "Bonjour Aya, oui votre candidature est actuellement "
                "en cours d'etude."
            ),
            is_read=False,
        )

        # =========================================================
        # NOTIFICATIONS - CANDIDATE 1
        # =========================================================

        Notification.objects.create(
            user=candidate1,
            type=Notification.NotificationType.APPLICATION,
            title="Candidature envoyee",
            message=(
                "Votre candidature pour le poste "
                "Developpeur Full Stack a ete envoyee."
            ),
            link=f"/applications/{application1.id}",
            is_read=True,
        )

        Notification.objects.create(
            user=candidate1,
            type=Notification.NotificationType.APPLICATION_STATUS,
            title="Candidature acceptee",
            message=(
                "Votre candidature pour le poste "
                "Developpeur Full Stack a ete acceptee."
            ),
            link=f"/applications/{application1.id}",
            is_read=False,
        )

        Notification.objects.create(
            user=candidate1,
            type=Notification.NotificationType.APPLICATION_STATUS,
            title="Entretien",
            message=(
                "Votre candidature pour le poste "
                "Developpeur Backend Django passe a l'etape entretien."
            ),
            link=f"/applications/{application2.id}",
            is_read=False,
        )

        # =========================================================
        # NOTIFICATIONS - CANDIDATE 2
        # =========================================================

        Notification.objects.create(
            user=candidate2,
            type=Notification.NotificationType.APPLICATION,
            title="Candidature envoyee",
            message=(
                "Votre candidature pour le poste "
                "Developpeur Backend Django a ete envoyee."
            ),
            link=f"/applications/{application3.id}",
            is_read=True,
        )

        Notification.objects.create(
            user=candidate2,
            type=Notification.NotificationType.MESSAGE,
            title="Nouveau message",
            message=(
                "Vous avez recu un nouveau message du recruteur."
            ),
            link="/chat",
            is_read=False,
        )

        # =========================================================
        # NOTIFICATIONS - RECRUITERS
        # =========================================================

        Notification.objects.create(
            user=recruiter1,
            type=Notification.NotificationType.APPLICATION,
            title="Nouvelle candidature",
            message=(
                "Mohamed Yassine a postule a votre offre "
                "Developpeur Full Stack."
            ),
            link=f"/recruiter/applications/{application1.id}",
            is_read=False,
        )

        Notification.objects.create(
            user=recruiter2,
            type=Notification.NotificationType.APPLICATION,
            title="Nouvelle candidature",
            message=(
                "Mohamed Yassine a postule a votre offre "
                "Developpeur Backend Django."
            ),
            link=f"/recruiter/applications/{application2.id}",
            is_read=False,
        )

        Notification.objects.create(
            user=recruiter2,
            type=Notification.NotificationType.APPLICATION,
            title="Nouvelle candidature",
            message=(
                "Aya El Idrissi a postule a votre offre "
                "Developpeur Backend Django."
            ),
            link=f"/recruiter/applications/{application3.id}",
            is_read=False,
        )

        Notification.objects.create(
            user=recruiter3,
            type=Notification.NotificationType.APPLICATION,
            title="Nouvelle candidature",
            message=(
                "Aya El Idrissi a postule a votre offre "
                "Developpeur Frontend React."
            ),
            link=f"/recruiter/applications/{application4.id}",
            is_read=False,
        )

        # =========================================================
        # SUCCESS SUMMARY
        # =========================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "=============================================="
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "       JOBCONNECT DATABASE SEEDED"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "=============================================="
            )
        )

        self.stdout.write("")

        self.stdout.write("USERS")
        self.stdout.write("----------------------------------------------")

        self.stdout.write(
            "ADMIN       : admin@jobconnect.com / Admin123!"
        )

        self.stdout.write(
            "RECRUITER 1 : recruiter1@jobconnect.com / Recruiter123!"
        )

        self.stdout.write(
            "RECRUITER 2 : recruiter2@jobconnect.com / Recruiter123!"
        )

        self.stdout.write(
            "RECRUITER 3 : recruiter3@jobconnect.com / Recruiter123!"
        )

        self.stdout.write(
            "CANDIDATE 1 : candidate1@jobconnect.com / Candidate123!"
        )

        self.stdout.write(
            "CANDIDATE 2 : candidate2@jobconnect.com / Candidate123!"
        )

        self.stdout.write("")

        self.stdout.write("DATA")
        self.stdout.write("----------------------------------------------")

        self.stdout.write("Users        : 6")
        self.stdout.write("Companies    : 3")
        self.stdout.write("Recruiters   : 3")
        self.stdout.write("Candidates   : 2")
        self.stdout.write("Skills       : 12")
        self.stdout.write("Job offers   : 3")
        self.stdout.write("Applications : 4")
        self.stdout.write("Favorites    : 2")
        self.stdout.write("Conversations: 2")
        self.stdout.write("Messages     : 5")
        self.stdout.write("Notifications: 9")

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Base de donnees remplie avec succes."
            )
        )