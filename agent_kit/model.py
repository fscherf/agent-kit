import os

from ollama import Client


class Model:
    separator = "__"
    models = {}

    @classmethod
    def get_identifier(cls):
        if not cls.models:
            cls.discover()

        return list(cls.models.keys())

    @classmethod
    def get(cls, model_identifier):
        if not cls.models:
            cls.discover()

        model_spec = cls.models[model_identifier]

        model = model_spec["model_class"](
            **model_spec["model_kwargs"],
        )

        model.identifier = model_identifier
        model.name = model_spec["model_name"]

        return model

    @classmethod
    def discover(cls):
        def _register_models(prefix, model, model_kwargs):
            for model_name in model.get_models_names().keys():
                model_identifier = f"{prefix}{cls.separator}{model_name}"

                cls.models[model_identifier] = {
                    "model_class": model.__class__,
                    "model_kwargs": model_kwargs,
                    "model_name": model_name,
                }

        cls.models.clear()

        # Ollama local
        ollama_url = os.environ.get("OLLAMA_URL", "")

        if ollama_url:
            model_kwargs = {
                "host": ollama_url,
            }

            try:
                model = Ollama(**model_kwargs)

                _register_models(
                    prefix="ollama-local",
                    model=model,
                    model_kwargs=model_kwargs,
                )

            except Exception:
                pass

        # Ollama Cloud
        ollama_api_key = os.environ.get("OLLAMA_CLOUD_API_KEY", "")

        if ollama_url:
            model_kwargs = {
                "host": "https://ollama.com",
                "api_key": ollama_api_key,
            }

            try:
                model = Ollama(**model_kwargs)

                _register_models(
                    prefix="ollama-cloud",
                    model=model,
                    model_kwargs=model_kwargs,
                )

            except Exception:
                pass

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.identifier!r})>"


