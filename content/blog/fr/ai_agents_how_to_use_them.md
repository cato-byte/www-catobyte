## Les agents IA en 2026 : comment ils fonctionnent et comment bien les utiliser, avec Claude, Codex et les autres

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Les agents IA en 2026](../../images/ai_agents_how_to_use_them_title_img.png)

*Article technique*

## Des chatbots aux agents

Un chatbot répond et attend. Un agent reçoit un objectif, décide quoi faire, utilise des outils, examine les résultats et continue jusqu'à atteindre l'objectif ou rester bloqué. Des agents de code comme Claude Code et Codex modifient désormais des dépôts, lancent les tests et ouvrent des pull requests tout seuls, et chaque fournisseur cloud vend une plateforme pour construire des agents de support client, d'exploitation et de travail sur les données.

Dans un [article précédent](ai_agents_and_data_engineering.html), j'ai examiné ce que les agents changent pour les équipes de data engineering : ce qu'elles leur délèguent, les risques et l'évolution du métier. Celui-ci est plus pratique. Il explique comment fonctionnent les agents et quels patrons de conception recommandent les principaux laboratoires, puis comment bien utiliser les deux outils avec lesquels je travaille tous les jours, Claude Code et Codex. Il s'appuie sur [Building effective agents](https://www.anthropic.com/research/building-effective-agents) d'Anthropic, le [guide des agents](https://developers.openai.com/api/docs/guides/agents) d'OpenAI, la [présentation de l'IA agentique](https://aws.amazon.com/ai/agentic-ai/) d'AWS et la documentation officielle de chaque outil. Les exemples de prompts et de fichiers de configuration sont en anglais, comme on les écrit dans les vrais projets.

## Qu'est-ce qu'un agent ?

Anthropic trace une frontière utile entre deux types de systèmes « agentiques » :

- **Les workflows** : des systèmes où les modèles de langage et les outils sont orchestrés par des chemins de code prédéfinis. Votre code décide des étapes ; le modèle les remplit.
- **Les agents** : des systèmes où le modèle dirige dynamiquement son propre processus et l'usage des outils, en gardant la main sur la façon d'accomplir la tâche.

La définition d'OpenAI correspond à la seconde : des systèmes capables de planifier et d'accomplir des tâches avec des outils, de travailler avec d'autres agents et de garder le contexte d'une étape à l'autre. Au fond, un agent est étonnamment simple. Selon Anthropic, les agents sont « en général de simples LLM qui utilisent des outils en fonction des retours de leur environnement, dans une boucle » :

```python
def run_agent(goal: str, tools: dict, max_steps: int = 30) -> str:
    messages = [{"role": "user", "content": goal}]
    for _ in range(max_steps):                      # a stopping condition
        reply = call_model(messages, tools=list(tools))
        messages.append(reply)
        if not reply.tool_calls:                    # the model considers the goal reached
            return reply.text
        for call in reply.tool_calls:               # act, then observe the result
            result = tools[call.name](**call.arguments)
            messages.append({"role": "tool", "id": call.id, "content": result})
    return "Stopped: step limit reached"
```

Tout ce qui rend un vrai agent bon ou mauvais se joue autour de cette boucle : quels outils existent et comment ils sont décrits, ce que le modèle voit dans son contexte, comment il vérifie son propre travail, ce qu'il peut faire sans demander et quand il s'arrête.

## Commencer simple : quand faut-il un agent ?

Anthropic et OpenAI donnent le même premier conseil : utiliser la solution la plus simple qui fonctionne. Un seul appel au modèle, bien rédigé, avec de la recherche documentaire et quelques exemples, suffit pour beaucoup d'applications. Les agents échangent latence et coût contre de la flexibilité, et Anthropic prévient que leur autonomie entraîne « des coûts plus élevés et un risque d'erreurs qui s'accumulent » : une mauvaise étape au début sert de base à toutes les suivantes.

Les agents valent leur coût sur des problèmes ouverts, dont on ne peut prévoir le nombre d'étapes ni coder un chemin fixe, et dont les résultats sont vérifiables. C'est pourquoi le code est aujourd'hui le cas d'usage le plus solide : les tests et les builds indiquent à l'agent s'il a réussi. Le support client est l'autre cas mis en avant par Anthropic, car le succès s'y mesure en demandes résolues.

## Les patrons

L'article d'Anthropic décrit une échelle de patrons, des workflows figés aux agents autonomes. Ce sont des briques à combiner, pas un framework :

| Patron | Fonctionnement | À utiliser quand | Exemple en data engineering |
|---|---|---|---|
| LLM augmenté | Un appel avec recherche, outils et mémoire | La plupart des tâches ; la base de tout le reste | Répondre aux questions sur une table grâce au catalogue |
| Chaînage de prompts | Suite fixe d'appels, avec des contrôles entre les étapes | La tâche se découpe proprement en étapes | Rédiger la doc dbt, la confronter au SQL, corriger |
| Routage | Classer l'entrée et l'envoyer vers un traitement spécialisé | Des catégories distinctes traitées différemment | Envoyer erreurs de schéma et d'infrastructure vers des runbooks différents |
| Parallélisation | Sous-tâches indépendantes en même temps, ou plusieurs votes | Vitesse, ou confiance accrue par plusieurs regards | Relire une migration sous l'angle exactitude, performance et sécurité en parallèle |
| Orchestrateur et exécutants | Un modèle découpe la tâche et délègue les sous-tâches qu'il choisit | Les sous-tâches ne sont pas connues à l'avance | Renommer une colonne dans tous les modèles et dashboards qui l'utilisent |
| Évaluateur et optimiseur | Un modèle produit, un autre critique, en boucle | Des critères clairs et un gain mesurable à itérer | Optimiser une requête lente jusqu'à ce que le benchmark passe |
| Agent autonome | Le modèle planifie et agit en boucle avec des outils | Tâches ouvertes dans un environnement sûr et vérifiable | Analyser et corriger un job nocturne en échec |

Les trois principes d'Anthropic valent quel que soit l'outil : garder une conception **simple**, rendre la planification de l'agent **transparente** et soigner l'**interface agent-ordinateur** en documentant et en testant les outils.

## Les outils sont l'interface de l'agent

Un agent ne peut pas être meilleur que ses outils. Anthropic raconte qu'en construisant son agent de code pour SWE-bench, l'équipe a passé plus de temps à optimiser les outils que le prompt général. Son conseil : concevoir les outils pour le modèle comme une fonction pour un développeur junior, avec un nom clair, une description qui donne des exemples d'usage et des cas limites, et des paramètres qui rendent les erreurs difficiles (ce qu'elle appelle le *poka-yoke*). Dans un cas, le modèle se trompait avec des chemins relatifs après avoir changé de répertoire ; exiger des chemins absolus a réglé le problème.

Une définition d'outil écrite avec ce soin :

```json
{
  "name": "run_sql_readonly",
  "description": "Run a read-only SQL query on the analytics warehouse and return at most 200 rows as CSV. Use it to inspect data, check row counts or validate a transformation. Only SELECT and WITH statements are accepted; anything else is rejected. Always filter large fact tables by date, because unfiltered scans time out after 60 seconds. Table names must be fully qualified, for example analytics.marts.fct_orders.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "A single SELECT or WITH statement with fully qualified table names."},
      "reason": {"type": "string", "description": "One sentence on what you expect to learn from this query."}
    },
    "required": ["query", "reason"]
  }
}
```

La contrainte de lecture seule est dans l'outil, pas seulement dans sa description ; la limite de lignes protège la fenêtre de contexte ; le champ `reason` rend l'intention de l'agent visible dans les logs.

## Les briques communes

Quelques standards fonctionnent désormais d'un outil à l'autre, et valent d'être appris une fois :

- **MCP (Model Context Protocol)** relie les agents à des outils et des données (gestionnaires de tickets, bases de données, fichiers de design, API internes) via des serveurs utilisables par tout agent compatible. Anthropic l'a créé et l'a confié en décembre 2025 à la nouvelle [Agentic AI Foundation](https://sdtimes.com/ai/linux-foundation-forms-agentic-ai-foundation-to-be-new-home-for-mcp-goose-and-agents-md/) de la Linux Foundation.
- **Les fichiers de contexte** contiennent les consignes qu'un agent lit au début de chaque session : `CLAUDE.md` pour Claude Code, `AGENTS.md` pour Codex et beaucoup d'autres agents. AGENTS.md, créé par OpenAI, a rejoint la même fondation.
- **Les skills** regroupent une connaissance métier ou un workflow répétable dans un dossier avec un fichier `SKILL.md`, que l'agent ne charge que lorsqu'il en a besoin. Claude Code et Codex les prennent en charge.
- **Les sous-agents** exécutent une partie de la tâche dans leur propre fenêtre de contexte et renvoient un résumé, ce qui garde la conversation principale ciblée.

Pour construire ses propres agents, chaque laboratoire propose des couches qui échangent du contrôle contre du confort. Anthropic a la Messages API (vous écrivez la boucle), le [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) (la boucle, les outils et la gestion du contexte de Claude Code, sous forme de bibliothèque Python ou TypeScript) et [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) (un environnement hébergé où Anthropic exécute l'agent et son sandbox, pour les travaux de longue durée). OpenAI a la Responses API, l'Agents SDK (votre application exécute la boucle, avec outils et passages de relais entre agents) et l'Agents API (un environnement Codex hébergé avec compaction et orchestration multi-agents). AWS propose [Amazon Bedrock AgentCore](https://aws.amazon.com/ai/agentic-ai/) pour exécuter à grande échelle des agents construits avec n'importe quel framework ou modèle, avec mémoire, gouvernance et sécurité, ainsi que le Strands Agents SDK open source. La mise en garde d'Anthropic sur les frameworks vaut pour tous : beaucoup de patrons tiennent en quelques lignes sur l'API brute, et si vous utilisez un framework, comprenez ce qu'il fait en dessous, car les hypothèses erronées à son sujet sont une source fréquente de bugs.

## Claude : bien utiliser Claude Code

Claude Code est l'outil de code agentique d'Anthropic, disponible dans le terminal, les IDE, une application de bureau et le web. Son [guide des bonnes pratiques](https://code.claude.com/docs/en/best-practices) part d'une contrainte qui explique presque tous ses conseils : la fenêtre de contexte se remplit vite, et les performances baissent à mesure qu'elle se remplit. Chaque fichier lu et chaque sortie de commande prennent de la place : gérer le contexte est la compétence centrale.

**Donnez-lui un moyen de vérifier son travail.** C'est l'habitude la plus importante. Sans vérification qu'il peut lancer, « ça a l'air fini » est le seul signal dont dispose Claude, et c'est vous qui devenez la boucle de vérification. Avec des tests, un build, un linter ou une capture d'écran à comparer, il peut itérer jusqu'à ce que la vérification passe. Les exemples du guide :

```text
Before: implement a function that validates email addresses

After:  write a validateEmail function. example test cases: user@example.com is
        true, invalid is false, user@.com is false. run the tests after implementing
```

```text
Before: the build is failing

After:  the build fails with this error: [paste error]. fix it and verify the build
        succeeds. address the root cause, don't suppress the error
```

Sur les sessions longues, on peut rendre la vérification obligatoire : `/goal` fait travailler Claude jusqu'à ce qu'une condition soit remplie, un hook Stop peut l'empêcher de terminer tant qu'un script ne passe pas, et un sous-agent de vérification peut tenter de réfuter le résultat avec un regard neuf. Demandez des preuves, les commandes et leur sortie, plutôt que des affirmations de réussite.

**Explorer, planifier, puis coder.** Pour les changements qui touchent plusieurs fichiers ou du code que vous ne connaissez pas, utilisez le mode plan (`Shift+Tab`, ou `claude --permission-mode plan`) : Claude lit et propose un plan sans rien modifier. Relisez et corrigez le plan, puis laissez-le implémenter et committer. La règle du guide pour sauter cette étape : si vous pouvez décrire le diff en une phrase, demandez-le directement.

**Soyez précis.** Nommez les fichiers, les scénarios et les contraintes, et indiquez des patrons existants :

```text
users report that login fails after session timeout. check the auth flow in
src/auth/, especially token refresh. write a failing test that reproduces the
issue, then fix it
```

Pour les fonctionnalités plus importantes, le guide suggère de laisser Claude vous interviewer d'abord et rédiger une spécification dans un fichier, puis de l'implémenter dans une nouvelle session.

**Gardez un CLAUDE.md court et utile.** Claude le lit au début de chaque session. Lancez `/init` pour en générer une première version, puis ne gardez que ce que Claude ne peut pas déduire du code : commandes, règles de style différentes des conventions, consignes de test, usages du dépôt, pièges propres au projet. Pour chaque ligne, demandez-vous si la supprimer causerait des erreurs. Un fichier trop long fait que Claude en ignore la moitié.

```markdown
# Commands
- Tests: ./kunturvenv/bin/pytest -q (builds the site first)
- Never run scripts/deploy.sh; deployment happens in CI from master

# Conventions
- Content is written in US English first, then translated to es and fr
- Study guides live in content/guides, articles in content/blog
```

**Utilisez chaque point d'extension pour ce qu'il fait bien.** Les hooks sont déterministes, contrairement aux consignes : réservez-les à ce qui doit arriver à chaque fois, comme lancer un linter après chaque modification ou bloquer les écritures dans un dossier de migrations. Les skills (`.claude/skills/<nom>/SKILL.md`) contiennent des connaissances ou des workflows utiles de temps en temps. Les sous-agents (`.claude/agents/`) mènent les investigations dans un contexte séparé (« use subagents to investigate how our authentication handles token refresh »). Les serveurs MCP et les outils en ligne de commande comme `gh` ou `aws` le relient aux systèmes externes ; le guide note que les CLI sont le moyen le plus économe en contexte.

**Pilotez la session.** Appuyez sur `Esc` pour l'arrêter et le réorienter ; `Esc Esc` ou `/rewind` restaurent le code et la conversation depuis des points de contrôle antérieurs. Lancez `/clear` entre des tâches sans rapport. Si vous avez corrigé deux fois la même erreur, le contexte est encombré de tentatives ratées : videz-le et repartez avec un meilleur prompt.

**Réglez les permissions sciemment.** Les versions récentes démarrent en mode auto, où un classifieur séparé examine les actions et bloque celles qui sont risquées, comme l'élargissement de périmètre ou les actions provoquées par un contenu hostile. Les listes d'autorisations pré-approuvent les commandes de confiance, et le sandbox restreint l'accès au système de fichiers et au réseau au niveau du système d'exploitation. Le mode manuel demande avant chaque écriture ou commande.

**Passez à l'échelle quand vous êtes prêt.** `claude -p` s'exécute sans interaction dans des scripts et en CI, avec une sortie JSON. On peut répartir une migration sur de nombreux fichiers, lancer des sessions en parallèle dans des worktrees git distincts, ou former un binôme rédacteur/relecteur où une seconde session, au contexte vierge, relit ce qu'a écrit la première :

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from Python 2 to Python 3. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)" \
    --permission-mode dontAsk
done
```

Testez le prompt sur deux ou trois fichiers d'abord, corrigez ce qui coince, puis lancez le reste. Avant de considérer un travail sans surveillance comme terminé, faites relire le diff par un sous-agent au regard du plan, en ne signalant que les manques qui touchent à l'exactitude ou aux exigences, pour que la relecture ne pousse pas le code vers la sur-ingénierie.

## Codex : bien utiliser l'agent de code d'OpenAI

Codex est l'agent d'ingénierie logicielle d'OpenAI, disponible dans ChatGPT, une application de bureau, une CLI, une extension d'IDE et Codex Cloud, avec la revue de code sur GitHub. Son [guide de prompting](https://learn.chatgpt.com/codex/prompting) recommande les mêmes habitudes de fond, avec son propre vocabulaire.

**Nommez le comportement, le code et les contraintes.** Un bon prompt Codex dit ce qui doit changer, indique les fichiers ou étapes de reproduction pertinents, et précise ce qui ne doit pas changer :

```text
Users get a 500 when exporting reports with more than 10,000 rows. Start by
reproducing the bug locally with the fixture in tests/fixtures/big_report.csv, then
propose a patch and run checks. Do not change the API shape. Keep the fix minimal
and add a regression test if feasible.
```

Dans la CLI, référencez les chemins avec `@` ; dans l'IDE, les fichiers ouverts sont inclus automatiquement et les lignes sélectionnées délimitent la demande. Pour du travail d'interface, joignez des captures et précisez le framework et les conventions de composants, qu'une image ne montre pas.

**Planifiez, puis avancez par jalons.** Pour les tâches en plusieurs étapes, `/plan` fait enquêter Codex et proposer une approche avant toute modification ; on peut demander des révisions, comme les fichiers déplacés à chaque jalon et une stratégie de retour arrière. `/goal` fixe un objectif persistant quand il est disponible. Un gros travail avance un jalon à la fois, chacun relu avant le suivant.

**Demandez-lui de vérifier et de rendre compte.** Les exemples du guide : rejouer la reproduction après le correctif, lancer le linter et la plus petite suite de tests pertinente en indiquant les commandes et les résultats, démarrer le serveur de développement et donner l'URL à vérifier. Après avoir traité les retours d'une revue, relancez `/review`.

**Écrivez un AGENTS.md.** Codex lit un fichier global dans `~/.codex`, puis chaque `AGENTS.md` de la racine du dépôt jusqu'au répertoire courant ; les fichiers les plus proches du répertoire de travail l'emportent sur les précédents, jusqu'à 32 Kio par défaut. Mettez-y les conventions de travail (gestionnaire de paquets, tests à lancer), les attentes du dépôt (linter avant les pull requests) et les règles de revue de code près du code qu'elles concernent ; des fichiers imbriqués peuvent remplacer des commandes pour un service précis.

```markdown
# AGENTS.md
- Use uv; never pip install into the system Python.
- After changing pipeline code, run: uv run pytest tests/unit -q
- Run uv run ruff check . before opening a pull request.
- Never edit files under migrations/ by hand; generate them with make migration.

## Code Review Rules
- Flag any query on fct_* tables without a date filter.
```

**Choisissez le mode de permissions.** « Ask for approval » travaille dans l'espace de travail et s'arrête avant de modifier quoi que ce soit en dehors ou d'accéder à internet ; c'est le mode recommandé par défaut. « Approve for me » garde le même sandbox mais transmet les demandes d'approbation à un relecteur automatique qui ne s'arrête que sur les actions potentiellement dangereuses. « Full access » lève les restrictions. Le sandbox définit ce à quoi Codex peut accéder ; les approbations, quand il s'arrête.

**Déléguez en parallèle.** Codex Cloud exécute des tâches dans des environnements isolés pendant que vous continuez à travailler : planifiez en local, confiez « Implement Milestone 1 from the plan », relisez le diff et ouvrez une pull request. `codex exec` l'exécute sans interaction depuis des scripts. Petit exemple vécu : les images de couverture de cet article et des deux précédents ont été générées en appelant `codex exec` depuis un autre agent, avec un prompt décrivant chaque article et un répertoire temporaire où écrire, puis relues avant d'être ajoutées au site.

## Les autres agents à connaître

Les mêmes habitudes valent pour le reste du marché. GitHub Copilot propose un mode agent dans l'éditeur et un agent de code qui va des issues aux pull requests. Cursor est un éditeur pensé pour l'IA, avec des agents en arrière-plan. Gemini CLI de Google est un agent de terminal open source. Kiro, d'AWS, est un IDE construit autour du développement guidé par les spécifications, où exigences et documents de conception précèdent le code. Et les plateformes de données intègrent leurs propres agents, comme Cortex Code chez Snowflake et les fonctions agentiques de Lakeflow chez Databricks, qui s'appuient sur le catalogue et les droits de la plateforme. La plupart lisent `AGENTS.md` ou leur propre fichier de contexte, prennent en charge MCP et proposent une combinaison de mode plan, de niveaux de permissions et d'exécution en arrière-plan.

## Les pratiques qui marchent avec n'importe quel agent

Entre les ressources d'Anthropic, d'OpenAI et d'AWS et ma propre pratique, voici les habitudes qui font la différence :

1. **Donnez à l'agent une vérification qu'il peut lancer.** Tests, builds, linters, validations de données, captures d'écran. Pas de vérification, pas de travail sans surveillance.
2. **Écrivez le contexte, brièvement.** Un fichier de contexte court avec les commandes et les règles non évidentes, plus des skills pour les connaissances occasionnelles. Élaguez-le quand l'agent l'ignore.
3. **Planifiez avant les gros changements.** Séparez l'exploration de la modification et relisez le plan ; il coûte moins cher à corriger que le diff.
4. **Soyez précis sur le périmètre et les contraintes.** Fichiers, scénarios, ce qui ne doit pas changer, ce que « terminé » veut dire.
5. **Gardez le contexte propre.** Une tâche par session, des sous-agents pour les investigations, un nouveau départ après des corrections répétées.
6. **Moindre privilège.** Sandboxes, identifiants de développement, approbation de tout ce qui a des effets de bord ; jamais d'accès en écriture à la production pour un agent.
7. **Traitez le contenu externe comme non fiable.** Issues, pages web et fichiers peuvent porter une injection de prompt ; la vraie limite, ce sont les permissions de l'agent, pas son prompt.
8. **Relisez avec un regard neuf.** Une seconde session ou un sous-agent, ou un humain, relit le diff au regard des exigences avant la fusion.
9. **Parallélisez le travail indépendant.** Worktrees, tâches dans le cloud et scripts de répartition, chacun avec sa vérification.
10. **Mesurez le résultat.** Délai de livraison, défauts et reprises, pas l'impression de vitesse. AWS indique que des équipes internes qui ont repensé leur façon de travailler autour des agents ont livré en 76 jours, à six ingénieurs, un projet dimensionné pour 30 développeurs ; de tels résultats viennent d'un changement de méthode, pas seulement d'un nouvel outil.

La direction est claire : les agents passent du statut d'assistants que l'on surveille à celui de collègues à qui l'on délègue. Ce qui rend la délégation sûre est la même chose qu'avec des personnes : une tâche claire, le bon contexte, des permissions limitées, un moyen de vérifier le résultat et une relecture avant de le valider.

## Sources

- Anthropic : [Building effective agents](https://www.anthropic.com/research/building-effective-agents), [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)
- OpenAI : [Agents guide](https://developers.openai.com/api/docs/guides/agents), [Codex prompting](https://learn.chatgpt.com/codex/prompting), [Codex AGENTS.md](https://learn.chatgpt.com/codex/agent-configuration/agents-md), [Codex permissions](https://learn.chatgpt.com/codex/permission-modes)
- AWS : [Agentic AI on AWS](https://aws.amazon.com/ai/agentic-ai/)
- Linux Foundation : [Agentic AI Foundation, new home for MCP and AGENTS.md (SD Times)](https://sdtimes.com/ai/linux-foundation-forms-agentic-ai-foundation-to-be-new-home-for-mcp-goose-and-agents-md/)
