from django.contrib import admin

from .models import (
    GrammarRule,
    GrammarRuleAdmin,
    GrammarRuleComponent,
    GrammarRuleHumanVerifiedPromptExample,
    GrammarRuleHumanVerifiedPromptExampleAdmin,
    GrammarRuleExamplePrompt,
    GrammarRuleExample,
    GrammarRuleExampleAdmin,
    GrammarRuleExampleComponent,
)

admin.site.register(GrammarRule, GrammarRuleAdmin)
admin.site.register(GrammarRuleComponent)
admin.site.register(GrammarRuleHumanVerifiedPromptExample, GrammarRuleHumanVerifiedPromptExampleAdmin)
admin.site.register(GrammarRuleExamplePrompt)
admin.site.register(GrammarRuleExample, GrammarRuleExampleAdmin)
admin.site.register(GrammarRuleExampleComponent)
