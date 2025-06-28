# Testing different URLs

## Case 1: [Spotify support](https://support.spotify.com/in-en/)

```bash

[
  {
    "module": "Spotify Support",
    "Description": "Provides assistance and resources for Spotify users encountering issues or needing help with their accounts. Includes quick help for login issues, payment problems, and community support.",
    "Submodules": {
      "Quick Help": [
        "Can’t log in to Spotify",
        "Failed payment help",
        "Charged too much",
        "Invite or remove Family plan members",
        "How to change your payment details"
      ],
      "Visit our Community": "Find answers from the worldwide Community of expert fans.",
      "Failed Payment Help": [
        "Ensure payment method has sufficient funds",
        "Payment method must be registered in the same country as Spotify account",
        "Payment method should not be expired or canceled",
        "Payment method must be enabled for foreign, secure online, and recurring purchases",
        "Information on banks supporting recurring payments for Visa and Mastercard"
      ],
      "Payments through a Partner": "If your plan is with a partner company, they manage your payments. You need to speak to them about anything payment related."
    }
  },
  {
    "module": "Payment Management",
    "Description": "This module provides functionalities related to managing payments for Spotify accounts, including handling failed payments, managing payment methods, and understanding charges.",
    "Submodules": {
      "Recurring Payments": "Support for recurring payments with specific banks and card types.",
      "Failed Payment Handling": "Guidance on what to do if a regular payment fails, including retrying payments and maintaining Premium access.",
      "Payments through Partners": "Information on managing payments through partner companies, including how to contact them.",
      "Payment Details Management": "Instructions on how to check and update payment information, including viewing order history and receipts.",
      "Student Discount Management": "Details on managing the Premium Student plan, including renewal and eligibility.",
      "Tax and Charges": "Information on how taxes are applied to Premium plans and how to view a breakdown of charges."
    }
  },
  {
    "module": "Family Plan Management",
    "Description": "Manage and configure Spotify Family Plan memberships, including adding or removing members and troubleshooting issues.",
    "Submodules": {
      "Invite or Remove Family Plan Members": "The plan manager can add or remove members on their Family page.",
      "Address and Verification for Family Plan": "Confirm full address for plan members.",
      "Can't Join Family Plan": "Troubleshoot issues with joining the Family plan."
    }
  },
  {
    "module": "Spotify Account Management",
    "Description": "Manage your Spotify account, including payment and privacy settings.",
    "Submodules": {
      "Change Payment Details": "Update or change your payment details for Spotify.",
      "Payments through a Partner": "Manage payments if your plan is with a partner company.",
      "Remove Card Details": "Remove the token used to process your card data by canceling your plan.",
      "Saved Payment Cards": "Save and manage your payment details for future purchases."
    }
  }
]

```

## Case 2: [Cluely support](https://support.cluely.com/en/)

```bash

[
  {
    "module": "Getting Started",
    "Description": "Everything you need to get going. This section includes a quick guide on keyboard shortcuts, instructions on what to do if Cluely is not visible, and basic checks to verify if Cluely works on your system before subscribing.",
    "Submodules": {
      "How to use Cluely": "Quick guide on keyboard shortcuts & getting started.",
      "Can't see Cluely": "Instructions on what to do if Cluely is not visible.",
      "Downloading Cluely": "This guide will help you get up and running quickly.",
      "Basic Checks": "Verify if Cluely works on your system before subscribing."
    }
  },
  {
    "module": "Cluely",
    "Description": "Cluely is a tool that provides assistance and interaction through keyboard shortcuts and voice commands.",
    "Submodules": {
      "Keyboard Shortcuts": {
        "Toggle Visibility": "Press Command + Backslash (/) to toggle visibility of Cluely.",
        "Ask for Help": "Press Command + Enter to ask Cluely to help you with whatever is on your screen.",
        "Move Cluely": "Press Command + Arrow Right/Left to move Cluely around the screen.",
        "Scroll Conversations": "Press Command + Arrow Up/Down to scroll between conversations in Cluely History.",
        "Chat with Cluely": "Press Command + Shift + Enter to chat with Cluely for more guidance.",
        "Start Over": "Press Command + R to start over the conversation history."
      },
      "Voice and Audio Recording": {
        "Record Voice and Audio": "Click the microphone icon to start recording your voice and system audio, which will be sent to Cluely when you ask for help."
      },
      "Visibility Troubleshooting": {
        "Toggle Visibility": "Press \u001b + / to toggle visibility if the application is hidden.",
        "Restart Cluely": "Restart the application from Activity Monitor to ensure it is not moved off-screen."
      }
    }
  },
  {
    "module": "Cluely AI Summaries & Notes",
    "Description": "Release notes for Cluely version 1.5.0, detailing updates and new features.",
    "Submodules": {}
  }
]

```

## Case 3: [Redash support](https://redash.io/help/)

```bash

[
  {
    "module": "Querying",
    "Description": "Write queries effectively with the power and comfort of a SQL client and the collaborative advantages of a cloud-based service.",
    "Submodules": {
      "Powerful online SQL editor": "Provides a robust interface for writing SQL queries.",
      "Browse schema and click-to-insert": "Allows users to explore database schemas and insert elements into queries with ease.",
      "Create snippets and reuse them": "Enables users to create reusable code snippets for frequent use."
    }
  },
  {
    "module": "Visualization",
    "Description": "Easily visualize your results in various formats and create thematic dashboards.",
    "Submodules": {
      "Visualization Types": [
        "Charts: Line, Bar, Area, Pie, Scatter",
        "Boxplot",
        "Cohort",
        "Sunburst",
        "Word Cloud",
        "Sankey",
        "Map",
        "Counter",
        "Pivot Table",
        "Funnel"
      ],
      "Dashboard Sharing": [
        "Share dashboards on a URL",
        "Embed widgets anywhere"
      ]
    }
  },
  {
    "module": "Redash",
    "Description": "Redash is a data visualization and dashboarding tool that allows users to query multiple data sources, create visualizations, and share insights across teams.",
    "Submodules": {
      "Data Source Integration": "Ability to query multiple data sources from a single window, including Redshift, MySQL, and Data Lake via Athena.",
      "Dashboards": "Create and share dashboards that combine multiple queries into publicly viewable formats.",
      "Parameters and Filters": "Use parameters and filters to customize queries and visualizations.",
      "API": "Redash API allows for integration and automation of data workflows.",
      "Instance Creation": {
        "AWS EC2 AMI": "Launch instances using pre-baked AMIs for various regions.",
        "Google Compute Engine": "Create instances using Redash images on Google Cloud.",
        "Docker": "Deploy Redash using Docker and Docker Compose."
      }
    }
  },
  {
    "module": "Docker",
    "Description": "Docker setup and configuration for Redash, including environment setup and running instances.",
    "Submodules": {
      "Environment Setup": "Create a .env file and set secret keys for Redash.",
      "Running Instances": "Run Redash instances with API server, background workers, Redis, and PostgreSQL."
    }
  },
  {
    "module": "AWS",
    "Description": "Instructions for launching a Redash instance using AWS AMIs.",
    "Submodules": {
      "Launch Instance": "Use pre-baked AMI for small deployments (t2.small recommended).",
      "Security Group": "Allow incoming traffic on ports 22 (SSH), 80 (HTTP), and 443 (HTTPS).",
      "User Connection": "Use 'ubuntu' user for SSH connection."
    }
  },
  {
    "module": "Data Sources",
    "Description": "Redash supports querying data from various SQL, NoSQL, Big Data, and API data sources to answer complex issues.",
    "Submodules": {
      "Databases": [
        "Amazon Athena",
        "Amazon Aurora",
        "Amazon DynamoDB",
        "Amazon Redshift",
        "Axibase TSDB",
        "Azure Data Explorer (Kusto)",
        "Cassandra",
        "ClickHouse",
        "Databricks",
        "Druid",
        "Elasticsearch",
        "Google BigQuery",
        "Graphite",
        "Greenplum",
        "Hive",
        "Impala",
        "InfluxDB",
        "MemSQL",
        "Microsoft SQL Server",
        "MongoDB",
        "MySQL",
        "Oracle",
        "PostgreSQL",
        "Presto",
        "Rockset",
        "ScyllaDB",
        "Snowflake",
        "TreasureData",
        "Vertica"
      ],
      "Integrations": [
        "Google Analytics",
        "Google Spreadsheets",
        "JIRA",
        "JSON",
        "Python",
        "Salesforce",
        "Yandex AppMetrica",
        "Yandex Metrica"
      ],
      "Partners": [
        "Segment",
        "Snowplow Analytics",
        "Stitch"
      ]
    }
  }
]

```
