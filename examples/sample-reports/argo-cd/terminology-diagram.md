# Stem & Leaf — Argo CD Docs Terminology (docs/, excluding vendored docs/snyk)
Each card = one source using that term.
● unambiguous  ○ correct-in-context  △ ambiguous  ✕ conflict

════════════════════════════════════════════════════════════════════════
CORE OBJECT NAMES
════════════════════════════════════════════════════════════════════════

ApplicationSet      │ ● ApplicationSet        operator-manual/applicationset/…███░░░░░  68×
CRD/controller      │ △ AppSet △              operator-manual/feature-maturit…█░░░░░░░  9×
(the CRD/controller │ ✕ Appset △              operator-manual/applicationset/…█░░░░░░░  3×
that generates      │
multiple            │
Applications from   │
generators)         │

────────────────────────────────────────────────────────────────────────

AppProject CRD      │ ● AppProject            operator-manual/declarative-set…█░░░░░░░  32×
(the CRD that scopes│ △ Application Project △ user-guide/source-integrity.md  █░░░░░░░  1×
Applications and    │
RBAC/source/destina…│
restrictions)       │

────────────────────────────────────────────────────────────────────────

Git repository      │ ● Git repository        operator-manual/security.md     ██░░░░░░  42×
(source of truth)   │ ○ git repo              operator-manual/cluster-bootstr…█░░░░░░░  19×
(the external Git   │ ○ repo-server (componen…operator-manual/high_availabili…████████  210×
repo Argo CD syncs  │
manifests from)     │


════════════════════════════════════════════════════════════════════════
SYNC & OPERATIONS
════════════════════════════════════════════════════════════════════════

Application sync    │ ● OutOfSync             getting_started.md, index.md, a…█░░░░░░░  17×
status: OutOfSync   │ ○ out-of-sync           cluster-bootstrapping.md, upgra…█░░░░░░░  9×
(an Application     │ ○ out of sync           faq.md, cluster-bootstrapping.m…█░░░░░░░  7×
whose live state    │
deviates from its   │
desired Git state)  │

────────────────────────────────────────────────────────────────────────

Deploying to a      │ ● rollback              index.md, architecture.md, user…█░░░░░░░  16×
previous Git        │ ○ revert (different con…developer-guide/submit-your-pr.…█░░░░░░░  12×
revision            │
(restoring an       │
Application to a    │
prior deployed state│
via Argo CD's       │
history feature)    │

────────────────────────────────────────────────────────────────────────

Destination cluster │ ● destination cluster   operator-manual/secret-manageme…█░░░░░░░  13×
for a deployment    │ △ target cluster △      operator-manual/applicationset/…█░░░░░░░  11×
(the cluster an     │
Application's       │
resources are       │
deployed to         │
(spec.destination)) │

────────────────────────────────────────────────────────────────────────

Resource hook       │ ● resource hook         user-guide/annotations-and-labe…█░░░░░░░  1×
(a manifest         │ ○ Resource Hook (headin…applicationset/Progressive-Sync…█░░░░░░░  1×
annotated to run at │
a sync-lifecycle    │
point               │
(PreSync/Sync/PostS…│


════════════════════════════════════════════════════════════════════════
ABBREVIATIONS / AMBIGUOUS
════════════════════════════════════════════════════════════════════════

Config Management   │ ● Config Management Plu…operator-manual/config-manageme…█░░░░░░░  14×
Plugin              │ ● CMP (post-expansion s…operator-manual/config-manageme…█░░░░░░░  9×
(user-defined plugin│
that generates      │
manifests via a     │
custom tool)        │

────────────────────────────────────────────────────────────────────────

Single Sign-On      │ △ SSO (no expansion on …index.md, security_consideratio…█░░░░░░░  21×
authentication      │ ○ Single Sign-On (expan…operator-manual/security.md, us…█░░░░░░░  4×
(logging in once via│
an external         │
OIDC/OAuth2 identity│
provider)           │


════════════════════════════════════════════════════════════════════════
LEGEND
════════════════════════════════════════════════════════════════════════
● Clearly scoped — unambiguous, correct for context
○ Technically correct but narrower than the stem
△ Ambiguous or inconsistent use
✕ Conflict — same word, incompatible meaning across sources

════════════════════════════════════════════════════════════════════════
⚠  THE CONFLICT THAT MATTERS MOST
════════════════════════════════════════════════════════════════════════
The 'Appset' casing used in the filename and prose of operator-manual/applicationset/Appset-Any-Namespace.md collides with the correct CRD name ApplicationSet and the accepted shorthand AppSet — a reader skimming could mistake it for a different, unofficial feature rather than a namespace-scoping capability of the same ApplicationSet CRD.

THE BEST EXISTING PRACTICE
docs/operator-manual/config-management-plugins.md is the most disciplined source: it defines 'Config Management Plugin (CMP)' once on first use and consistently uses the CMP shorthand afterward, which is the pattern the rest of the docs (especially SSO and ApplicationSet/AppSet usage) should copy.
