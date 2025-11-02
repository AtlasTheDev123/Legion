Canonical function catalog: 27 functions (see `schemas/functions_count.txt`)

# Function Reference (Full, generated)\n\nGenerated from schemas/functions.json — total functions: 27\n\n## setup_dev_environment\n\nCreate project scaffold, init venv/container, and install base dependencies.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: array\n\n**Required**: project, language\n\n**Example**:\n`json\n{
    "project":  "atlas-core",
    "language":  "python",
    "dependencies":  [
                         "fastapi",
                         "pydantic"
                     ]
}\n`\n\n## dependency_scan\n\nRun dependency/security scanner over a codebase.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: string\n\n**Required**: path, tool\n\n**Example**:\n`json\n{
    "path":  "/projects/atlas-core",
    "tool":  "safety",
    "severity":  "high"
}\n`\n\n## run_vulnerability_scan\n\nRun network/vulnerability scan inside an isolated lab (requires lab auth).\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: string\n\n**Required**: target, scan_profile, authorization_token\n\n**Example**:\n`json\n{
    "target":  "localhost",
    "scan_profile":  "full",
    "authorization_token":  "[REDACTED_LAB_AUTH]"
}\n`\n\n## create_remediation_patch\n\nGenerate a remediation patch or PR for a known vulnerability.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n\n**Required**: vuln_id, repo_path\n\n**Example**:\n`json\n{
    "vuln_id":  "VULN-001",
    "repo_path":  "/projects/atlas-core"
}\n`\n\n## run_port_scan\n\nPerform a port scan against a target host or network segment  ONLY with authorization and in isolated lab environments.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: string\n\n**Required**: target_ip, authorization_token\n\n**Example**:\n`json\n{
    "target_ip":  "127.0.0.1",
    "ports":  "1-1024",
    "authorization_token":  "[REDACTED_LAB_AUTH]"
}\n`\n\n## spawn_agent\n\nCreate and start an orchestration agent instance with supplied role and capabilities.\n\n**Parameters**:\n\n- $p: string\n- $p: array\n- $p: string\n\n**Required**: agent_name\n\n**Example**:\n`json\n{
    "agent_name":  "orchestrator-1",
    "capabilities":  [
                         "scan",
                         "report"
                     ],
    "run_mode":  "dry-run"
}\n`\n\n## spawn_subagent\n\nSpawn a short-lived sub-agent to perform a bounded task and return results to the parent agent.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: integer\n\n**Required**: parent_agent, task\n\n**Example**:\n`json\n{
    "parent_agent":  "orchestrator-1",
    "task":  "collect-logs",
    "max_runtime_seconds":  120
}\n`\n\n## analyze_logs\n\nAnalyze collected logs for suspicious patterns and summarize findings.\n\n**Parameters**:\n\n- $p: array\n- $p: string\n\n**Required**: log_paths\n\n**Example**:\n`json\n{
    "log_paths":  [
                      "/var/log/auth.log"
                  ],
    "time_window":  "24h"
}\n`\n\n## monitor_logs\n\nStart continuous log monitoring with alerting rules (read-only unless authorized).\n\n**Parameters**:\n\n- $p: array\n- $p: array\n\n**Required**: sources\n\n**Example**:\n`json\n{
    "sources":  [
                    "/var/log/syslog",
                    "/var/log/app.log"
                ],
    "alert_rules":  [
                        "failed-login",
                        "high-cpu"
                    ]
}\n`\n\n## generate_forensics_playbook\n\nProduce a forensics playbook for a detected incident with step-by-step actions.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n\n**Required**: incident_id, severity\n\n**Example**:\n`json\n{
    "incident_id":  "INC-001",
    "severity":  "high"
}\n`\n\n## create_incident_response_runbook\n\nGenerate a runnable incident response runbook with commands and play steps.\n\n**Parameters**:\n\n- $p: string\n- $p: array\n\n**Required**: incident_id, systems\n\n**Example**:\n`json\n{
    "incident_id":  "INC-001",
    "systems":  [
                    "web-01",
                    "db-01"
                ]
}\n`\n\n## rotate_secrets\n\nRotate credentials or secrets via secret-store APIs. Requires secure vault permissions and audit.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: boolean\n\n**Required**: secret_id, vault\n\n**Example**:\n`json\n{
    "secret_id":  "svc/db-user",
    "vault":  "azure-key-vault",
    "force":  false
}\n`\n\n## deploy_application\n\nDeploy an application artifact to a target environment (staging/production) using approved pipelines.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: string\n\n**Required**: artifact_id, environment\n\n**Example**:\n`json\n{
    "artifact_id":  "atlas-core:1.2.3",
    "environment":  "staging",
    "strategy":  "canary"
}\n`\n\n## monitor_performance\n\nCollect and summarize performance metrics for services over a time window.\n\n**Parameters**:\n\n- $p: string\n- $p: array\n- $p: string\n\n**Required**: service, metrics\n\n**Example**:\n`json\n{
    "service":  "atlas-api",
    "metrics":  [
                    "cpu",
                    "latency"
                ],
    "time_window":  "1h"
}\n`\n\n## generate_architecture_diagram\n\nProduce a system architecture diagram (textual or mermaid) from code / infra descriptions.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n\n**Required**: source\n\n**Example**:\n`json\n{
    "source":  "infra/tf",
    "format":  "mermaid"
}\n`\n\n## create_bug_bounty_scope\n\nDraft an authorized bug bounty program scope and disclosure guidelines for a product or service.\n\n**Parameters**:\n\n- $p: string\n- $p: array\n- $p: array\n- $p: array\n\n**Required**: product_name, in_scope, out_of_scope\n\n**Example**:\n`json\n{
    "product_name":  "Atlas Core",
    "in_scope":  [
                     "api.example.com"
                 ],
    "out_of_scope":  [
                         "admin.example.com"
                     ],
    "reward_tiers":  [
                         {
                             "severity":  "critical",
                             "reward_usd":  2000
                         }
                     ]
}\n`\n\n## generate_supplemental_docs_for_audit\n\nProduce documentation artifacts required for compliance audits (evidence mapping, config snapshots, control descriptions).\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: array\n\n**Required**: compliance_standard, unit\n\n**Example**:\n`json\n{
    "compliance_standard":  "ISO27001",
    "unit":  "payments",
    "evidence_paths":  [
                           "/audit/evidence/2025-10"
                       ]
}\n`\n\n## create_access_token_policy\n\nDraft a policy for short-lived access tokens, lifetimes, scopes, and rotation rules.\n\n**Parameters**:\n\n- $p: integer\n- $p: array\n- $p: integer\n\n**Required**: token_lifetime_minutes, scopes\n\n**Example**:\n`json\n{
    "token_lifetime_minutes":  60,
    "scopes":  [
                   "read:logs",
                   "write:deploy"
               ],
    "rotation_frequency_days":  7
}\n`\n\n## generate_privilege_escalation_hunt\n\nCreate detection rules and hunt playbooks for common privilege escalation patterns.\n\n**Parameters**:\n\n- $p: string\n- $p: array\n\n**Required**: environment\n\n**Example**:\n`json\n{
    "environment":  "aws",
    "deliverables":  [
                         "sigma_rule",
                         "playbook.md"
                     ]
}\n`\n\n## create_privacy_data_map\n\nMap personal data flows across systems and produce retention and minimization recommendations.\n\n**Parameters**:\n\n- $p: array\n- $p: array\n\n**Required**: systems, data_types\n\n**Example**:\n`json\n{
    "systems":  [
                    "auth-service",
                    "marketing-db"
                ],
    "data_types":  [
                       "email",
                       "ssn"
                   ]
}\n`\n\n## generate_backup_strategy\n\nDesign a backup and restore strategy including retention, encryption, and recovery objectives.\n\n**Parameters**:\n\n- $p: array\n- $p: integer\n- $p: integer\n\n**Required**: systems, rpo_hours, rto_hours\n\n**Example**:\n`json\n{
    "systems":  [
                    "db-primary"
                ],
    "rpo_hours":  1,
    "rto_hours":  4
}\n`\n\n## create_malware_analysis_lab\n\nDesign an isolated analysis lab environment with VM/container specs, network isolation, and tooling lists.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: array\n\n**Required**: lab_name, isolation_level\n\n**Example**:\n`json\n{
    "lab_name":  "malware-lab-1",
    "isolation_level":  "vm",
    "tools":  [
                  "cuckoo",
                  "ghidra"
              ]
}\n`\n\n## generate_malicious_sample_handling_policy\n\nDraft safe handling and storage policies for potentially malicious samples, including chain-of-custody and retention.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: string\n\n**Required**: organization_name, responsible_team\n\n**Example**:\n`json\n{
    "organization_name":  "ATLAS",
    "responsible_team":  "ThreatOps",
    "storage_requirements":  "encrypted, airgapped"
}\n`\n\n## create_privileged_account_onboarding\n\nProduce an onboarding checklist and required controls for privileged accounts.\n\n**Parameters**:\n\n- $p: string\n- $p: array\n\n**Required**: account_type, required_controls\n\n**Example**:\n`json\n{
    "account_type":  "ops_admin",
    "required_controls":  [
                              "mfa",
                              "just-in-time",
                              "audit_logging"
                          ]
}\n`\n\n## generate_compliance_gap_analysis\n\nCompare current controls to a target compliance standard and produce prioritized remediation items.\n\n**Parameters**:\n\n- $p: string\n- $p: array\n\n**Required**: standard, evidence_paths\n\n**Example**:\n`json\n{
    "standard":  "SOC2",
    "evidence_paths":  [
                           "/audit/logs"
                       ]
}\n`\n\n## create_change_management_plan\n\nCreate a change management plan with approval flows, rollback criteria, and communication steps.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: array\n\n**Required**: change_id, impact_level, stakeholders\n\n**Example**:\n`json\n{
    "change_id":  "CHG-123",
    "impact_level":  "medium",
    "stakeholders":  [
                         "ops",
                         "sec"
                     ]
}\n`\n\n## generate_runbook_for_operation\n\nProduce an operational runbook with step-by-step commands, diagnostics, and recovery procedures for routine operations.\n\n**Parameters**:\n\n- $p: string\n- $p: string\n- $p: array\n\n**Required**: operation_name, platform\n\n**Example**:\n`json\n{
    "operation_name":  "monthly_backup_validate",
    "platform":  "k8s",
    "checklist":  [
                      "verify-snapshots",
                      "restore-test"
                  ]
}\n`\n\n
