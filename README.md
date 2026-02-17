# TELE-Analyst
#### Video Demo: https://youtu.be/49jPNZjugKs
#### Description: 

TELE-Analyst is an innovative AI-powered recruitment automation platform that bridges the gap between modern communication tools and traditional HR processes. Designed specifically for HR specialists, recruiters, and talent acquisition teams, this application addresses one of the most time-consuming challenges in hiring: the manual screening and evaluation of candidate resumes. By seamlessly integrating Telegram messenger capabilities with cutting-edge artificial intelligence, TELE-Analyst transforms the way organizations handle incoming job applications, providing instant, data-driven insights that accelerate decision-making while maintaining objectivity and consistency in candidate evaluation.

The core problem this platform solves is the bottleneck created when HR teams receive dozens or hundreds of CVs for open positions. Traditional manual review is not only time-intensive but also prone to human bias and inconsistency. TELE-Analyst automates this entire workflow: candidates submit their CVs directly through Telegram, the system processes them using Google's Gemini AI, evaluates skills against predefined criteria, and presents structured analytics on an interactive web dashboard—all happening in real-time without any manual intervention.

**Backend Architecture and Design Patterns**

The backend is built on Flask, a lightweight yet powerful Python web framework, and employs a sophisticated multi-layered architecture that prioritizes maintainability, scalability, and testability. At its foundation, the application implements three crucial design patterns that work in harmony to create a robust and extensible system.

The Repository Pattern forms the data access layer, providing a clean abstraction between business logic and database operations. Each domain entity—users, candidates, rules, and analytic records—has its own repository class (UserRepository, CandidateRepository, RuleRepository, AnalyticRecordRepository) that encapsulates all SQL queries and database interactions. This abstraction means the business logic never directly interacts with SQLite, making it trivial to swap databases or modify data structures without cascading changes throughout the codebase.

Building on this foundation, the Service Layer Pattern encapsulates all business logic and orchestrates operations across multiple repositories. Services like UserService, RuleService, CandidateService, and AnalyticRecordService contain the application's core functionality—user authentication, rule management, candidate processing, and analytics generation. This layer ensures business rules are consistently applied and provides a clear API for controllers to interact with, maintaining separation of concerns and making the codebase significantly more maintainable.

The Factory Pattern manages dependency injection through RepositoryFactory and ServiceFactory classes. Rather than controllers directly instantiating repositories and services, factories handle object creation and dependency wiring. This approach centralizes configuration, reduces coupling between components, and makes testing straightforward since mock objects can be injected through factories.

Perhaps the most sophisticated component is the TelegramMessagerService, which implements a multi-threaded asynchronous architecture to handle Telegram events without blocking the Flask application. This service runs asyncio event loops in separate daemon threads, allowing it to maintain persistent connections to Telegram while the main Flask thread handles HTTP requests. The advantage of using asyncio for Telegram event processing is critical: it enables non-blocking concurrent handling of multiple incoming messages, file downloads, and AI processing tasks. When a candidate sends a CV, the system can simultaneously handle other incoming documents, process API calls to Google Gemini, and push updates to the web interface—all without any request waiting for others to complete.

**Data Flow and Processing Pipeline**

The application follows a well-defined data flow from user configuration to final analytics presentation. HR users authenticate through a session-based system managed by Flask-Session, then navigate to the configuration page where they create screening rules by specifying technology tags (e.g., "Python, React, Docker"). These rules, stored via RuleService, define the evaluation criteria for incoming CVs.

When a candidate sends a CV document through Telegram, the TelegramMessagerService receives the event through Telethon (a Python Telegram client library). The handler downloads the document, uploads it to Google Gemini API using the generate_content function from the CVProcessingService, and receives back a structured JSON response containing technology ratings on a 1-5 scale. The service then creates or retrieves the candidate record through CandidateService and stores the complete analysis through AnalyticRecordService, linking it to the appropriate user, rule, and candidate.

**Frontend Architecture**

The frontend is built with Tailwind CSS, providing a responsive and modern user interface without heavy JavaScript frameworks. The interface consists of authentication modals for registration and login, a configuration page for managing screening rules, and an interactive dashboard that displays analytics in a sortable, filterable table format. Real-time updates are achieved through Socket.IO, establishing WebSocket connections between the browser and Flask server. When new CV analyses are completed, the backend emits events that instantly update the dashboard without requiring page refreshes, giving HR teams immediate visibility into new candidate submissions.

**Architectural Advantages and Extensibility**

The chosen architecture provides numerous benefits that position TELE-Analyst for long-term success. The layered structure with clear separation of concerns makes the system highly scalable—new features can be added by creating new services and repositories without modifying existing code. The repository abstraction means migrating from SQLite to PostgreSQL or MongoDB requires changes only in repository implementations, not throughout the entire application. The service layer's encapsulation of business logic makes comprehensive unit testing straightforward, as services can be tested independently with mock repositories.

The factory pattern's dependency management means new functionality can be integrated seamlessly. For example, adding support for WhatsApp or Slack would involve creating new messenger service implementations while reusing the existing rule, candidate, and analytics infrastructure. Similarly, the AI analysis could be extended to evaluate soft skills, cultural fit, or red flags by adding new service methods without disrupting existing functionality.

The multi-threaded asyncio architecture ensures the application remains responsive under load. Even with dozens of candidates submitting CVs simultaneously, the asynchronous processing prevents any single operation from blocking others, maintaining consistent performance and user experience. This design choice demonstrates forward-thinking engineering that anticipates real-world usage patterns where multiple recruiters and numerous candidates interact with the system concurrently.

TELE-Analyst represents a sophisticated integration of modern web technologies, messaging platforms, and artificial intelligence, all structured through battle-tested design patterns that ensure the codebase remains maintainable, testable, and extensible as requirements evolve and the user base grows.

**Telegram Account Configuration**

The system's ability to receive and process CVs relies on integrating a Telegram user account as the primary receiver. This integration is achieved through the Telethon library, a sophisticated Python implementation of Telegram's MTProto protocol that provides full access to Telegram's client API. Unlike bot accounts which have limited capabilities and cannot participate in regular user conversations, a user account can receive documents from candidates in private messages, group chats, or channels, making it ideal for recruitment scenarios.

The authentication process involves several critical components. First, the application requires Telegram API credentials (API_ID and API_HASH) which must be obtained by registering an application at https://my.telegram.org. These credentials identify your application to Telegram's servers and are necessary for any programmatic access to the Telegram network. The phone number associated with the Telegram account that will receive CVs must be provided, as Telegram's authentication is phone-based rather than username-based.

The TelegramConnectUser class handles the authentication flow through a multi-step process. When initializing the connection, the system can work with either a persistent session file (session_name) or a string-based session (StringSession). Session files store authentication tokens locally, allowing the application to maintain authenticated connections across restarts without requiring repeated login procedures. String sessions serve the same purpose but encode the session data as a string, making them portable and suitable for containerized deployments or cloud environments where file persistence might be challenging.

The initial authentication requires phone verification. When connecting for the first time, Telegram sends a verification code to the registered phone number via SMS or the official Telegram app. This code must be provided to complete the authentication through the sign_in method. If the account has two-factor authentication (2FA) enabled, an additional password verification step is required. The system gracefully handles this scenario by detecting the SessionPasswordNeededError, requesting the password hint, and prompting for the password to complete authentication.

Once authenticated, the TelegramClient maintains a persistent connection to Telegram's servers, listening for incoming events through the event handler system. The TelegramMessagerService registers custom handlers that trigger when new documents arrive, specifically filtering for messages containing file attachments. This event-driven architecture means the system reacts instantly to incoming CVs without polling or manual checks, ensuring minimal latency between submission and processing.

The multi-client architecture also supports adding multiple Telegram accounts, enabling HR departments to scale their operations across different recruiters or departments. Each client operates independently with its own event handlers and processing pipeline, managed through the TelegramMessagerService's client registry. This design allows organizations to segment candidate flows by job category, department, or region while maintaining centralized analytics and management through the unified web dashboard.

From a security perspective, session data and authentication tokens are sensitive credentials that grant full access to the Telegram account. The system stores these securely through environment variables (configured in the .env file), preventing hard-coded credentials in the source code. In production deployments, these credentials should be managed through secure configuration management systems or secret stores to prevent unauthorized access.


## How to start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   python -m pip install -r requirements.txt
   ```

2. Run the Flask app:
   ```
   python .\src\tgmp\main.py
   ```

   Or, if you want auto-reload during development:
   ```
   export FLASK_APP=src:app
   export FLASK_ENV=development
   flask run
   ```
   (On Windows, use `set` instead of `export`.)

The API will be available at http://127.0.0.1:5000/


