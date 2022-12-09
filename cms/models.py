from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


# Wagtail Block Documentation : https://docs.wagtail.org/en/stable/reference/streamfield/blocks.html

class TitleBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre")
    large = blocks.BooleanBlock(label="Large", required=False)


class ImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre", required=False)
    image = ImageChooserBlock(label="Illustration")
    alt = blocks.CharBlock(label="Texte alternatif (description textuelle de l'image)", required=False)
    caption = blocks.CharBlock(label="Légende", required=False)
    url = blocks.URLBlock(label="Lien", required=False)


class CoverImage(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre")
    text = blocks.CharBlock(label="Texte")
    cta_label = blocks.CharBlock(label="Texte du bouton", required=False)
    cta_link = blocks.URLBlock(label="Lien du bouton", required=False)


class ImageAndTextBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Illustration (à gauche)")
    image_ratio = blocks.ChoiceBlock(label="Largeur de l'image", choices=[
        ('3', '3/12'), ('5', '5/12'), ('6', '6/12'),
    ])
    text = blocks.RichTextBlock(label="Texte avec mise en forme (à droite)")
    link_label = blocks.CharBlock(
        label="Titre du lien",
        help_text="Le lien apparait en bas du bloc de droite, avec une flèche",
        required=False
    )
    link_url = blocks.URLBlock(label="Lien", required=False)


level_choices = [
    ('error', 'Erreur'),
    ('success', 'Succès'),
    ('info', 'Information'),
    ('warning', 'Attention'),
]


class AlertBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre du message", required=False)
    description = blocks.TextBlock(label="Texte du message", required=False)
    level = blocks.ChoiceBlock(label="Type de message", choices=level_choices)


color_choices = [
    ('', 'Bleu/Gris'),
    ('fr-callout--brown-caramel', 'Marron'),
    ('fr-callout--green-emeraude', 'Vert'),
]


class CalloutBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre de la mise en vant", required=False)
    text = blocks.TextBlock(label="Texte mis en avant", required=False)
    color = blocks.ChoiceBlock(label="Couleur", choices=color_choices, required=False)


class QuoteBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Illustration (à gauche)")
    quote = blocks.CharBlock(label="Citation")
    author_name = blocks.CharBlock(label="Nom de l'auteur")
    author_title = blocks.CharBlock(label="Titre de l'auteur")


class NumberBlock(blocks.StructBlock):
    number = blocks.CharBlock(label="Chiffre")
    label = blocks.CharBlock(label="Texte du chiffre")
    info = blocks.CharBlock(label="Texte d'information", required=False)


class NumbersBlock(blocks.StreamBlock):
    title = blocks.CharBlock(label="Titre", required=True)
    image = ImageBlock(label="Image", required=False)
    number = NumberBlock(label="Chiffre", min_num=3, max_num=4)


class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre", required=False)
    caption = blocks.CharBlock(label="Légende")
    url = blocks.URLBlock(label="Lien de la vidéo", help_text="URL au format 'embed' (Ex. : https://www.youtube.com/embed/gLzXOViPX-0)")


badge_level_choices = [
    ('error', 'Erreur'),
    ('success', 'Succès'),
    ('info', 'Information'),
    ('warning', 'Attention'),
    ('new', 'Nouveau'),
    ('grey', 'Gris'),
    ('green-emeraude', 'Vert'),
    ('blue-ecume', 'Bleu'),
]


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre")
    text = blocks.TextBlock(label="Texte")
    image = ImageChooserBlock(label="Image")
    url = blocks.URLBlock(label="Lien", required=False)

    badge_text = blocks.CharBlock(label="Texte du badge", required=False)
    badge_level = blocks.ChoiceBlock(label="Type de badge", choices=badge_level_choices, required=False)
    badge_icon = blocks.BooleanBlock(label="Masquer l'icon du badge", required=False)


svg_icon_choices = [
    ('avatar', 'Jeunesse'),
    ('coding', 'Numérique'),
    ('community', 'Communication'),
    ('environment', 'Climat et biodiversité'),
    ('france-localization', 'Logement'),
    ('health', 'Notre santé'),
    ('human-cooperation', 'Bien vieillir'),
    ('map', 'Assises du travail'),
    ('money', 'Modèle productif et social'),
    ('notification', 'Notification'),
    ('school', 'Notre école'),
    ('document-download', 'Document'),
]


class BadgeBlock(blocks.StructBlock):
    text = blocks.CharBlock(label="Texte du badge", required=False)
    color = blocks.ChoiceBlock(label="Couleur de badge", choices=badge_level_choices, required=False)
    hide_icon = blocks.BooleanBlock(label="Masquer l'icon du badge", required=False)


class BadgesListBlock(blocks.StreamBlock):
    badge = BadgeBlock(label="Badge")


class TileBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre", required=False)
    text = blocks.TextBlock(label="Texte", required=False)
    url = blocks.URLBlock(label="Lien", required=False)
    svg_icon = blocks.ChoiceBlock(label="Image d'illustration", choices=svg_icon_choices, required=False)
    badges = BadgesListBlock(label="Badges")


class CardHorizontalBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre")
    text = blocks.TextBlock(label="Texte")
    document = DocumentChooserBlock(label="Document", required=False)
    svg_icon = blocks.ChoiceBlock(label="Image d'illustration", choices=svg_icon_choices, required=False)
    ratio = blocks.ChoiceBlock(label="Largeur", choices=[('6', '6/12'), ('12', '12/12')])


class MultiColumnsBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(label="Texte avec mise en forme")
    image = ImageBlock(label="Image")
    video = VideoBlock(label="Vidéo")
    card = CardBlock(label="Carte")
    tile = TileBlock(label="Tuile thématique")
    cardhorizontal = CardHorizontalBlock(label="Carte Document")
    quote = QuoteBlock(label="Citation")


class QuestionBlock(blocks.StructBlock):
    question = blocks.CharBlock(label="Question")
    answer = blocks.RichTextBlock(label="Réponse")


class FaqBlock(blocks.StreamBlock):
    title = blocks.CharBlock(label="Titre")
    question = QuestionBlock(label="Question", min_num=1, max_num=15)


class ParticipantsListBlock(blocks.StreamBlock):
    participant = blocks.CharBlock(label="Participant")


class TilesListBlock(blocks.StreamBlock):
    tile = TileBlock(label="Tuile thématique")


class MultiTilesBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre", required=True)
    ratio = blocks.ChoiceBlock(label="Largeur des tuiles thématique", choices=[
         ('3', '3/12'), ('4', '4/12'), ('6', '6/12'),
    ])
    tiles = TilesListBlock(label="Thématique",)


class TilesAndParticipantsBlock(blocks.StructBlock):
    ratio = blocks.ChoiceBlock(label="Largeur de la colonne thématique", choices=[
         ('6', '6/12'), ('8', '8/12'),
    ])
    tilestitle = blocks.CharBlock(label="Titre des thématiques")
    tiles = TilesListBlock(label="Les thématiques")
    participantstitle = blocks.CharBlock(label="Titre des participants")
    participants = ParticipantsListBlock(label="Les participants")


class StepBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre de l'étape")
    detail = blocks.TextBlock(label="Détail")


class StepsListBlock(blocks.StreamBlock):
    step = StepBlock(label="Étape")


class StepperBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre")
    total = blocks.IntegerBlock(label="Nombre d'étape")
    current = blocks.IntegerBlock(label="Étape en cours")
    steps = StepsListBlock(label="Les étapes")


class FooterJeParticipeBlock(blocks.StructBlock):
    pass


class ContentPage(Page):

    body = StreamField([
        ('cover', CoverImage(label="Image pleine largeur avec texte (homepage)")),
        ('title', TitleBlock(label="Titre de page")),
        ('paragraph', blocks.RichTextBlock(label="Texte avec mise en forme")),
        ('paragraphlarge', blocks.RichTextBlock(label="Texte avec mise en forme (large)")),
        ('image', ImageBlock()),
        ('imageandtext', ImageAndTextBlock(label="Bloc image à gauche et texte à droite")),
        ('alert', AlertBlock(label="Message d'alerte")),
        ('callout', CalloutBlock(label="Texte mise en avant")),
        ('quote', QuoteBlock(label="Citation")),
        ('numbers', NumbersBlock(label="Chiffres")),
        ('video', VideoBlock(label="Vidéo")),
        ('multicolumns', MultiColumnsBlock(label="Multi-colonnes")),
        ('faq', FaqBlock(label="Questions fréquentes")),
        ('cardhorizontal', CardHorizontalBlock(label="Carte Document")),
        ('participantlist', ParticipantsListBlock(label="Liste de participants")),
        ('tilesparticipants', TilesAndParticipantsBlock(label="Thématiques & participants")),
        ('stepper', StepperBlock(label="Étapes")),
        ('multitiles', MultiTilesBlock(label="Les thématiques")),
        ('jeparticipe', FooterJeParticipeBlock(label="Bandeau Je participe")),
    ], blank=True, use_json_field=True)

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
