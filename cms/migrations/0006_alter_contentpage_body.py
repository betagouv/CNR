# Generated by Django 3.2.16 on 2022-12-09 15:42

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_alter_contentpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='body',
            field=wagtail.fields.StreamField([('cover', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre')), ('text', wagtail.blocks.CharBlock(label='Texte')), ('cta_label', wagtail.blocks.CharBlock(label='Texte du bouton', required=False)), ('cta_link', wagtail.blocks.URLBlock(label='Lien du bouton', required=False))], label='Image pleine largeur avec texte (homepage)')), ('title', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre')), ('large', wagtail.blocks.BooleanBlock(label='Large', required=False))], label='Titre de page')), ('paragraph', wagtail.blocks.RichTextBlock(label='Texte avec mise en forme')), ('paragraphlarge', wagtail.blocks.RichTextBlock(label='Texte avec mise en forme (large)')), ('image', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Illustration')), ('alt', wagtail.blocks.CharBlock(label="Texte alternatif (description textuelle de l'image)", required=False)), ('caption', wagtail.blocks.CharBlock(label='Légende', required=False)), ('url', wagtail.blocks.URLBlock(label='Lien', required=False))])), ('imageandtext', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Illustration (à gauche)')), ('image_ratio', wagtail.blocks.ChoiceBlock(choices=[('3', '3/12'), ('5', '5/12'), ('6', '6/12')], label="Largeur de l'image")), ('text', wagtail.blocks.RichTextBlock(label='Texte avec mise en forme (à droite)')), ('link_label', wagtail.blocks.CharBlock(help_text='Le lien apparait en bas du bloc de droite, avec une flèche', label='Titre du lien', required=False)), ('link_url', wagtail.blocks.URLBlock(label='Lien', required=False))], label='Bloc image à gauche et texte à droite')), ('alert', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre du message', required=False)), ('description', wagtail.blocks.TextBlock(label='Texte du message', required=False)), ('level', wagtail.blocks.ChoiceBlock(choices=[('error', 'Erreur'), ('success', 'Succès'), ('info', 'Information'), ('warning', 'Attention')], label='Type de message'))], label="Message d'alerte")), ('callout', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre de la mise en vant', required=False)), ('text', wagtail.blocks.TextBlock(label='Texte mis en avant', required=False)), ('color', wagtail.blocks.ChoiceBlock(choices=[('', 'Bleu/Gris'), ('fr-callout--brown-caramel', 'Marron'), ('fr-callout--green-emeraude', 'Vert')], label='Couleur', required=False))], label='Texte mise en avant')), ('quote', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Illustration (à gauche)')), ('quote', wagtail.blocks.CharBlock(label='Citation')), ('author_name', wagtail.blocks.CharBlock(label="Nom de l'auteur")), ('author_title', wagtail.blocks.CharBlock(label="Titre de l'auteur"))], label='Citation')), ('numbers', wagtail.blocks.StreamBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=True)), ('image', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Illustration')), ('alt', wagtail.blocks.CharBlock(label="Texte alternatif (description textuelle de l'image)", required=False)), ('caption', wagtail.blocks.CharBlock(label='Légende', required=False)), ('url', wagtail.blocks.URLBlock(label='Lien', required=False))], label='Image', required=False)), ('number', wagtail.blocks.StructBlock([('number', wagtail.blocks.CharBlock(label='Chiffre')), ('label', wagtail.blocks.CharBlock(label='Texte du chiffre')), ('info', wagtail.blocks.CharBlock(label="Texte d'information", required=False))], label='Chiffre', max_num=4, min_num=3))], label='Chiffres')), ('video', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=False)), ('caption', wagtail.blocks.CharBlock(label='Légende')), ('url', wagtail.blocks.URLBlock(label='Lien de la vidéo'))], label='Vidéo')), ('multicolumns', wagtail.blocks.StreamBlock([('text', wagtail.blocks.RichTextBlock(label='Texte avec mise en forme')), ('image', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Illustration')), ('alt', wagtail.blocks.CharBlock(label="Texte alternatif (description textuelle de l'image)", required=False)), ('caption', wagtail.blocks.CharBlock(label='Légende', required=False)), ('url', wagtail.blocks.URLBlock(label='Lien', required=False))], label='Image')), ('video', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=False)), ('caption', wagtail.blocks.CharBlock(label='Légende')), ('url', wagtail.blocks.URLBlock(label='Lien de la vidéo'))], label='Vidéo')), ('card', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre')), ('text', wagtail.blocks.TextBlock(label='Texte')), ('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('url', wagtail.blocks.URLBlock(label='Lien', required=False)), ('badge_text', wagtail.blocks.CharBlock(label='Texte du badge', required=False)), ('badge_level', wagtail.blocks.ChoiceBlock(choices=[('error', 'Erreur'), ('success', 'Succès'), ('info', 'Information'), ('warning', 'Attention'), ('new', 'Nouveau')], label='Type de badge', required=False)), ('badge_icon', wagtail.blocks.BooleanBlock(label="Masquer l'icon du badge", required=False))], label='Carte')), ('tile', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=False)), ('text', wagtail.blocks.TextBlock(label='Texte', required=False)), ('url', wagtail.blocks.URLBlock(label='Lien', required=False)), ('svg_icon', wagtail.blocks.ChoiceBlock(choices=[('avatar', 'Jeunesse'), ('coding', 'Numérique'), ('community', 'Communication'), ('environment', 'Climat et biodiversité'), ('france-localization', 'Logement'), ('health', 'Notre santé'), ('human-cooperation', 'Bien vieillir'), ('map', 'Assises du travail'), ('money', 'Modèle productif et social'), ('notification', 'Notification'), ('school', 'Notre école')], label="Image d'illustration", required=False))], label='Tuile thématique')), ('cardhorizontal', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre')), ('text', wagtail.blocks.TextBlock(label='Texte')), ('document', wagtail.documents.blocks.DocumentChooserBlock(label='Document', required=False)), ('svg_icon', wagtail.blocks.ChoiceBlock(choices=[('avatar', 'Jeunesse'), ('coding', 'Numérique'), ('community', 'Communication'), ('environment', 'Climat et biodiversité'), ('france-localization', 'Logement'), ('health', 'Notre santé'), ('human-cooperation', 'Bien vieillir'), ('map', 'Assises du travail'), ('money', 'Modèle productif et social'), ('notification', 'Notification'), ('school', 'Notre école')], label="Image d'illustration", required=False))], label='Carte Document'))], label='Multi-colonnes')), ('faq', wagtail.blocks.StreamBlock([('title', wagtail.blocks.CharBlock(label='Titre')), ('question', wagtail.blocks.StructBlock([('question', wagtail.blocks.CharBlock(label='Question')), ('answer', wagtail.blocks.RichTextBlock(label='Réponse'))], label='Question', max_num=15, min_num=1))], label='Questions fréquentes')), ('cardhorizontal', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre')), ('text', wagtail.blocks.TextBlock(label='Texte')), ('document', wagtail.documents.blocks.DocumentChooserBlock(label='Document', required=False)), ('svg_icon', wagtail.blocks.ChoiceBlock(choices=[('avatar', 'Jeunesse'), ('coding', 'Numérique'), ('community', 'Communication'), ('environment', 'Climat et biodiversité'), ('france-localization', 'Logement'), ('health', 'Notre santé'), ('human-cooperation', 'Bien vieillir'), ('map', 'Assises du travail'), ('money', 'Modèle productif et social'), ('notification', 'Notification'), ('school', 'Notre école')], label="Image d'illustration", required=False))], label='Carte Document')), ('participantlist', wagtail.blocks.StreamBlock([('participant', wagtail.blocks.CharBlock(label='Participant'))], label='Liste de participants')), ('tilesparticipants', wagtail.blocks.StructBlock([('ratio', wagtail.blocks.ChoiceBlock(choices=[('6', '6/12'), ('8', '8/12')], label='Largeur de la colonne thématique')), ('tilestitle', wagtail.blocks.CharBlock(label='Titre des thématiques')), ('tiles', wagtail.blocks.StreamBlock([('tile', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=False)), ('text', wagtail.blocks.TextBlock(label='Texte', required=False)), ('url', wagtail.blocks.URLBlock(label='Lien', required=False)), ('svg_icon', wagtail.blocks.ChoiceBlock(choices=[('avatar', 'Jeunesse'), ('coding', 'Numérique'), ('community', 'Communication'), ('environment', 'Climat et biodiversité'), ('france-localization', 'Logement'), ('health', 'Notre santé'), ('human-cooperation', 'Bien vieillir'), ('map', 'Assises du travail'), ('money', 'Modèle productif et social'), ('notification', 'Notification'), ('school', 'Notre école')], label="Image d'illustration", required=False))], label='Tuile thématique'))], label='Les thématiques')), ('participantstitle', wagtail.blocks.CharBlock(label='Titre des participants')), ('participants', wagtail.blocks.StreamBlock([('participant', wagtail.blocks.CharBlock(label='Participant'))], label='Les participants'))], label='Thématiques & participants')), ('stepper', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre')), ('total', wagtail.blocks.IntegerBlock(label="Nombre d'étape")), ('current', wagtail.blocks.IntegerBlock(label='Étape en cours')), ('steps', wagtail.blocks.StreamBlock([('step', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label="Titre de l'étape")), ('detail', wagtail.blocks.TextBlock(label='Détail'))], label='Étape'))], label='Les étapes'))], label='Étapes')), ('multitiles', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=True)), ('ratio', wagtail.blocks.ChoiceBlock(choices=[('3', '3/12'), ('4', '4/12'), ('6', '6/12')], label='Largeur des tuiles thématique')), ('tiles', wagtail.blocks.StreamBlock([('tile', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Titre', required=False)), ('text', wagtail.blocks.TextBlock(label='Texte', required=False)), ('url', wagtail.blocks.URLBlock(label='Lien', required=False)), ('svg_icon', wagtail.blocks.ChoiceBlock(choices=[('avatar', 'Jeunesse'), ('coding', 'Numérique'), ('community', 'Communication'), ('environment', 'Climat et biodiversité'), ('france-localization', 'Logement'), ('health', 'Notre santé'), ('human-cooperation', 'Bien vieillir'), ('map', 'Assises du travail'), ('money', 'Modèle productif et social'), ('notification', 'Notification'), ('school', 'Notre école')], label="Image d'illustration", required=False))], label='Tuile thématique'))], label='Thématique'))], label='Les thématiques')), ('jeparticipe', wagtail.blocks.StructBlock([], label='Bandeau Je participe'))], blank=True, use_json_field=True),
        ),
    ]