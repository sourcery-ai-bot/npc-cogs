from .base_help import (
    EMPTY_STRING,
    GLOBAL_CATEGORIES,
    CategoryConvert,
    Context,
    EmbedField,
    HelpSettings,
    _,
    pagify,
)
import functools

# An attempt to reduce redundant code as much as possible in themes
class ThemesCompiler:
    @staticmethod
    async def bot_help(**kwargs):
        async def outer(fn):
            @functools.wraps(fn)
            async def inner(*args, **kwargs):
                description = ctx.bot.description or ""
                tagline = (help_settings.tagline) or self.get_default_tagline(ctx)
                if not await ctx.embed_requested():  # Maybe redirect to non-embed minimal format
                    await ctx.send("You need to enable embeds to use custom help menu")
                else:
                    emb = {
                        "embed": {"title": "", "description": ""},
                        "footer": {"text": ""},
                        "fields": [],
                    }

                    emb["footer"]["text"] = tagline
                    emb["embed"]["description"] = description
                    emb["title"] = f"{ctx.me.name} Help Menu"
                    # Maybe add category desc somewhere?
                    for cat in GLOBAL_CATEGORIES:
                        if cat.cogs and await self.blacklist(ctx, cat.name):
                            fn(**locals())

                    pages = await self.make_embeds(ctx, emb, help_settings=help_settings)
                    if get_pages:
                        return pages
                    else:
                        await self.send_pages(
                            ctx,
                            pages,
                            embed=True,
                            help_settings=help_settings,
                            add_emojis=((await self.config.settings())["react"]) and True,
                        )

            return inner

        return outer

    @classmethod
    def compile(cls):
        pass