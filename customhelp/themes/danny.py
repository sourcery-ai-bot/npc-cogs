from ..abc import ThemesMeta
from ..core.base_help import (
    EMPTY_STRING,
    GLOBAL_CATEGORIES,
    CategoryConvert,
    Context,
    EmbedField,
    HelpSettings,
    _,
    pagify,
)

from ..core.compiler import ThemesCompiler as compiler


class DannyHelp(ThemesMeta):
    """Inspired from R.danny's help menu"""

    @compiler.compile
    async def format_bot_help(
        self, ctx: Context, help_settings: HelpSettings, get_pages: bool = False
    ):
        def callback(*args, **kwargs):
            title = (str(cat.reaction) + " " if cat.reaction else "") + cat.name.capitalize()
            emb["fields"].append(
                EmbedField(
                    title,
                    f"`{ctx.clean_prefix}help {cat.name}`\n{cat.long_desc if cat.long_desc else ''}",
                    True,
                )
            )
            return locals()

        return callback(**locals())

    async def format_category_help(
        self,
        ctx: Context,
        obj: CategoryConvert,
        help_settings: HelpSettings,
        get_pages: bool = False,
    ):
        coms = await self.get_category_help_mapping(ctx, obj, help_settings=help_settings)
        if not coms:
            return
        description = ctx.bot.description or ""
        tagline = (help_settings.tagline) or self.get_default_tagline(ctx)

        if await ctx.embed_requested():

            emb = {
                "embed": {"title": "", "description": ""},
                "footer": {"text": ""},
                "fields": [],
            }

            emb["footer"]["text"] = tagline
            if description:
                emb["embed"]["title"] = f"*{description[:250]}*"
            for cog_name, data in coms:
                if cog_name:
                    title = f"**{cog_name}**"
                else:
                    title = _("**No Category:**")

                cog_text = " ".join((f"`{name}`") for name, command in sorted(data.items()))

                for page in pagify(cog_text, page_length=256, delims=[" "], shorten_by=0):
                    field = EmbedField(title, page, True)
                    emb["fields"].append(field)

            pages = await self.make_embeds(ctx, emb, help_settings=help_settings)
            if get_pages:
                return pages
            else:
                await self.send_pages(
                    ctx,
                    pages,
                    embed=True,
                    help_settings=help_settings,
                )

        else:
            await ctx.send("Please have embeds enabled")
