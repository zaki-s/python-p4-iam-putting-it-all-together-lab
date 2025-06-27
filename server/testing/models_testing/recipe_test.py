import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Recipe, User

class TestRecipe:
    '''User in models.py'''

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''

        with app.app_context():

            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(username="ChefHam")
            user.password_hash = "testpassword"  # required for _password_hash
            db.session.add(user)
            db.session.commit()

            recipe = Recipe(
                title="Delicious Shed Ham",
                instructions="""Or kind rest bred with am shed then. In""" + \
                    """ raptures building an bringing be. Elderly is detract""" + \
                    """ tedious assured private so to visited. Do travelling""" + \
                    """ companions contrasted it. Mistress strongly remember""" + \
                    """ up to. Ham him compass you proceed calling detract.""" + \
                    """ Better of always missed we person mr. September""" + \
                    """ smallness northward situation few her certainty""" + \
                    """ something.""",
                minutes_to_complete=60,
                user_id=user.id  # ✅ associate recipe with existing user
            )

            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter(Recipe.title == "Delicious Shed Ham").first()

            assert new_recipe.title == "Delicious Shed Ham"
            assert new_recipe.instructions.startswith("Or kind rest bred")
            assert new_recipe.minutes_to_complete == 60

    def test_requires_title(self):
        '''requires each record to have a title.'''

        with app.app_context():

            Recipe.query.delete()
            db.session.commit()

            recipe = Recipe(
                instructions="x" * 60,
                minutes_to_complete=10,
                user_id=1  # dummy value if table has a user
            )

            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        with app.app_context():

            Recipe.query.delete()
            db.session.commit()

            with pytest.raises((IntegrityError, ValueError)):
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="idk lol",
                    minutes_to_complete=20,
                    user_id=1  # dummy user_id again
                )
                db.session.add(recipe)
                db.session.commit()
