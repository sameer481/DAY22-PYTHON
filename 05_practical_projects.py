"""
================================================================================
Day 22: Python Object-Oriented Programming - Production Projects & Architectures
================================================================================
This script integrates all polymorphism paradigms (Duck Typing, Subtype
Polymorphism, Abstract Base Classes, Protocols, and Dunder Methods) into three
enterprise-grade production architectures:

Project 1: Enterprise Omnichannel Incident Alert & Notification Engine
Project 2: Multi-Format Business Intelligence Data Export Pipeline
Project 3: Universal E-Commerce Payment Gateway & Checkout Engine
================================================================================
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def print_separator(title: str) -> None:
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 75)
    print(f" {title}")
    print("=" * 75)


# ==============================================================================
# PROJECT 1: ENTERPRISE OMNICHANNEL INCIDENT ALERT SYSTEM
# ==============================================================================
# In production cloud infrastructures (like AWS or Azure), an incident
# notification engine must dispatch urgent alerts across diverse channels
# (Slack, SMS, Email, Mobile Push) uniformly without coupling the core alert
# generator to any single vendor SDK.

print_separator("PROJECT 1: Enterprise Omnichannel Incident Alert Engine")

@dataclass
class AlertPayload:
    incident_id: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    service_name: str
    summary: str
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


@dataclass
class DispatchReceipt:
    channel: str
    status: str
    delivered_to: str
    reference_id: str
    message: str


class NotificationChannel(ABC):
    """Abstract polymorphic interface that every delivery channel must fulfill."""

    @property
    @abstractmethod
    def channel_name(self) -> str:
        """Name of the communication channel."""
        pass

    @abstractmethod
    def dispatch(self, alert: AlertPayload) -> DispatchReceipt:
        """Deliver the alert and return a standardized receipt."""
        pass


class EmailNotificationChannel(NotificationChannel):
    def __init__(self, smtp_server: str, recipient_email: str):
        self.smtp_server = smtp_server
        self.recipient_email = recipient_email

    @property
    def channel_name(self) -> str:
        return "SMTP-Email"

    def dispatch(self, alert: AlertPayload) -> DispatchReceipt:
        ref_id = f"email_{alert.incident_id}_{hash(self.recipient_email) % 10000}"
        return DispatchReceipt(
            channel=self.channel_name,
            status="DELIVERED",
            delivered_to=self.recipient_email,
            reference_id=ref_id,
            message=f"Sent HTML email to {self.recipient_email} with subject: [{alert.severity}] {alert.service_name}"
        )


class SMSNotificationChannel(NotificationChannel):
    def __init__(self, gateway_provider: str, oncall_phone: str):
        self.gateway_provider = gateway_provider
        self.oncall_phone = oncall_phone

    @property
    def channel_name(self) -> str:
        return f"SMS-Gateway ({self.gateway_provider})"

    def dispatch(self, alert: AlertPayload) -> DispatchReceipt:
        ref_id = f"sms_{alert.incident_id}_99"
        # Simulate SMS 160-char truncation
        condensed_text = f"ALERT {alert.severity}: {alert.service_name} - {alert.summary[:60]}..."
        return DispatchReceipt(
            channel=self.channel_name,
            status="DELIVERED",
            delivered_to=self.oncall_phone,
            reference_id=ref_id,
            message=f"Dispatched SMS to {self.oncall_phone}: '{condensed_text}'"
        )


class SlackWebhookChannel(NotificationChannel):
    def __init__(self, channel_name: str, webhook_url: str):
        self._channel_name = channel_name
        self.webhook_url = webhook_url

    @property
    def channel_name(self) -> str:
        return f"Slack #{self._channel_name}"

    def dispatch(self, alert: AlertPayload) -> DispatchReceipt:
        color = "#FF0000" if alert.severity == "CRITICAL" else "#FFA500"
        ref_id = f"slack_msg_{alert.incident_id}"
        return DispatchReceipt(
            channel=self.channel_name,
            status="DELIVERED",
            delivered_to=self.channel_name,
            reference_id=ref_id,
            message=f"Posted Block-Kit JSON card [Color: {color}] to {self.channel_name}"
        )


class MobilePushChannel(NotificationChannel):
    def __init__(self, device_token: str):
        self.device_token = device_token

    @property
    def channel_name(self) -> str:
        return "FCM-Push-Notification"

    def dispatch(self, alert: AlertPayload) -> DispatchReceipt:
        ref_id = f"fcm_push_{alert.incident_id}"
        return DispatchReceipt(
            channel=self.channel_name,
            status="DELIVERED",
            delivered_to=self.device_token[:12] + "...",
            reference_id=ref_id,
            message=f"Pushed high-priority silent notification with sound alert."
        )


class AlertDispatcherEngine:
    """
    Central dispatcher coordinating notifications polymorphically across
    registered communication channels.
    """
    def __init__(self):
        self._channels: List[NotificationChannel] = []

    def register_channel(self, channel: NotificationChannel) -> None:
        self._channels.append(channel)
        print(f"[Dispatcher] Registered channel: {channel.channel_name}")

    def broadcast_incident(self, alert: AlertPayload) -> List[DispatchReceipt]:
        print(f"\n[ALERT BROADCAST] Incident {alert.incident_id} [{alert.severity}] - {alert.service_name}")
        print(f"Summary: {alert.summary}")
        print("-" * 65)

        receipts: List[DispatchReceipt] = []
        # Polymorphic iteration: each channel dispatches according to its own implementation!
        for channel in self._channels:
            receipt = channel.dispatch(alert)
            receipts.append(receipt)
            print(f"  [+] {receipt.channel:<25} -> {receipt.message}")
        return receipts


dispatcher = AlertDispatcherEngine()
dispatcher.register_channel(EmailNotificationChannel("smtp.corp.internal", "devops-leads@company.com"))
dispatcher.register_channel(SMSNotificationChannel("Twilio", "+1-555-019-2834"))
dispatcher.register_channel(SlackWebhookChannel("incident-war-room", "https://hooks.slack.com/services/XYZ"))
dispatcher.register_channel(MobilePushChannel("fcm_token_a8f9c0b1e2"))

test_alert = AlertPayload(
    incident_id="INC-5021",
    severity="CRITICAL",
    service_name="Payment-Auth-Service",
    summary="Redis cluster node 3 memory pressure exceeded 95%. Latency spike on checkout."
)

dispatcher.broadcast_incident(test_alert)


# ==============================================================================
# PROJECT 2: MULTI-FORMAT BUSINESS INTELLIGENCE DATA EXPORTER
# ==============================================================================
# Business reporting pipelines must export tabular datasets to multiple target
# formats (JSON, CSV, Markdown Table, XML) depending on client requests.

print_separator("PROJECT 2: Multi-Format Data Export Pipeline")

class DataExporter(ABC):
    """Abstract base class establishing the contract for all data exporters."""

    @property
    @abstractmethod
    def file_extension(self) -> str:
        pass

    @property
    @abstractmethod
    def mime_type(self) -> str:
        pass

    @abstractmethod
    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        """Convert list of records into formatted text payload."""
        pass


class JSONDataExporter(DataExporter):
    @property
    def file_extension(self) -> str:
        return "json"

    @property
    def mime_type(self) -> str:
        return "application/json"

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        payload = {
            "metadata": {
                "report_title": title,
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "record_count": len(data)
            },
            "records": data
        }
        return json.dumps(payload, indent=2)


class CSVDataExporter(DataExporter):
    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

    @property
    def file_extension(self) -> str:
        return "csv"

    @property
    def mime_type(self) -> str:
        return "text/csv"

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        if not data:
            return ""
        headers = list(data[0].keys())
        lines = [self.delimiter.join(headers)]
        for row in data:
            lines.append(self.delimiter.join(str(row.get(h, "")) for h in headers))
        return "\n".join(lines)


class MarkdownTableExporter(DataExporter):
    @property
    def file_extension(self) -> str:
        return "md"

    @property
    def mime_type(self) -> str:
        return "text/markdown"

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        if not data:
            return f"### {title}\n*No data available*"
        headers = list(data[0].keys())
        col_names = [h.replace("_", " ").title() for h in headers]
        header_row = "| " + " | ".join(col_names) + " |"
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
        data_rows = [
            "| " + " | ".join(str(row.get(h, "")) for h in headers) + " |"
            for row in data
        ]
        return f"### {title}\n\n" + "\n".join([header_row, separator_row] + data_rows)


class XMLDataExporter(DataExporter):
    @property
    def file_extension(self) -> str:
        return "xml"

    @property
    def mime_type(self) -> str:
        return "application/xml"

    def export(self, data: List[Dict[str, Any]], title: str) -> str:
        sanitized_title = title.lower().replace(" ", "_")
        lines = [f'<?xml version="1.0" encoding="UTF-8"?>', f'<{sanitized_title}>']
        for row in data:
            lines.append("  <record>")
            for k, v in row.items():
                lines.append(f"    <{k}>{v}</{k}>")
            lines.append("  </record>")
        lines.append(f'</{sanitized_title}>')
        return "\n".join(lines)


# Sample Business Dataset
sales_dataset = [
    {"region": "North America", "quarter": "Q1", "revenue_usd": 1250000, "growth_pct": 14.2},
    {"region": "Europe",        "quarter": "Q1", "revenue_usd": 980000,  "growth_pct": 8.7},
    {"region": "Asia-Pacific",  "quarter": "Q1", "revenue_usd": 1420000, "growth_pct": 21.5},
    {"region": "Latin America", "quarter": "Q1", "revenue_usd": 410000,  "growth_pct": 11.3}
]

# Client Export Service
def generate_and_display_report(exporter: DataExporter, dataset: List[Dict[str, Any]], title: str) -> None:
    print(f"\n--- Exporting to [{exporter.mime_type}] (.{exporter.file_extension}) ---")
    formatted_output = exporter.export(dataset, title)
    print(formatted_output)


exporters: List[DataExporter] = [
    JSONDataExporter(),
    CSVDataExporter(),
    MarkdownTableExporter(),
    XMLDataExporter()
]

# Process dataset polymorphically across all exporters
for exp in exporters:
    generate_and_display_report(exp, sales_dataset, "Q1 Global Revenue Report")


# ==============================================================================
# PROJECT 3: UNIVERSAL E-COMMERCE PAYMENT PROCESSING & CHECKOUT GATEWAY
# ==============================================================================
# An e-commerce platform processes orders using diverse financial vendors
# (Stripe, PayPal, Crypto Wallet, Bank Transfer). Each processor implements
# a unified polymorphic transaction contract.

print_separator("PROJECT 3: Universal Payment Gateway & Checkout Engine")

@dataclass
class TransactionResult:
    success: bool
    transaction_id: str
    gateway_provider: str
    amount: float
    currency: str
    fee_incurred: float
    message: str


class PaymentGateway(ABC):
    """Abstract contract for all payment providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def authorize_and_capture(self, amount: float, currency: str, payment_details: Dict[str, Any]) -> TransactionResult:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> TransactionResult:
        pass


class StripeGateway(PaymentGateway):
    """Credit card gateway with flat fee + percentage model."""
    @property
    def provider_name(self) -> str:
        return "Stripe Payments"

    def authorize_and_capture(self, amount: float, currency: str, payment_details: Dict[str, Any]) -> TransactionResult:
        card_last4 = payment_details.get("card_number", "0000")[-4:]
        # Stripe Fee: 2.9% + $0.30
        fee = round((amount * 0.029) + 0.30, 2)
        tx_id = f"ch_stripe_{datetime.now().strftime('%H%M%S%f')[:10]}"
        return TransactionResult(
            success=True,
            transaction_id=tx_id,
            gateway_provider=self.provider_name,
            amount=amount,
            currency=currency,
            fee_incurred=fee,
            message=f"Successfully charged Card ending in {card_last4} via Stripe Elements."
        )

    def refund(self, transaction_id: str, amount: float) -> TransactionResult:
        return TransactionResult(
            success=True,
            transaction_id=f"re_{transaction_id}",
            gateway_provider=self.provider_name,
            amount=amount,
            currency="USD",
            fee_incurred=0.0,
            message=f"Refunded ${amount:.2f} for transaction {transaction_id}"
        )


class PayPalGateway(PaymentGateway):
    """PayPal express checkout via verified PayPal account email."""
    @property
    def provider_name(self) -> str:
        return "PayPal Express"

    def authorize_and_capture(self, amount: float, currency: str, payment_details: Dict[str, Any]) -> TransactionResult:
        paypal_email = payment_details.get("paypal_email", "unknown@user.com")
        # PayPal Fee: 3.49% + $0.49
        fee = round((amount * 0.0349) + 0.49, 2)
        tx_id = f"PAYID_{datetime.now().strftime('%H%M%S%f')[:10]}"
        return TransactionResult(
            success=True,
            transaction_id=tx_id,
            gateway_provider=self.provider_name,
            amount=amount,
            currency=currency,
            fee_incurred=fee,
            message=f"Authorized one-click token payment for account '{paypal_email}'."
        )

    def refund(self, transaction_id: str, amount: float) -> TransactionResult:
        return TransactionResult(
            success=True,
            transaction_id=f"REFUND_{transaction_id}",
            gateway_provider=self.provider_name,
            amount=amount,
            currency="USD",
            fee_incurred=0.0,
            message=f"Credited ${amount:.2f} back to PayPal wallet."
        )


class CryptoGateway(PaymentGateway):
    """Cryptocurrency blockchain payment gateway (Bitcoin / Ethereum)."""
    @property
    def provider_name(self) -> str:
        return "Web3 Crypto Gateway"

    def authorize_and_capture(self, amount: float, currency: str, payment_details: Dict[str, Any]) -> TransactionResult:
        wallet_address = payment_details.get("wallet_address", "0x000000000000")
        network_gas_fee = 2.50  # Fixed simulated network gas
        tx_id = f"0x{datetime.now().strftime('%H%M%S%f')[:12]}abcdef"
        return TransactionResult(
            success=True,
            transaction_id=tx_id,
            gateway_provider=self.provider_name,
            amount=amount,
            currency=currency,
            fee_incurred=network_gas_fee,
            message=f"Verified 6 block confirmations from wallet {wallet_address[:8]}...{wallet_address[-4:]}."
        )

    def refund(self, transaction_id: str, amount: float) -> TransactionResult:
        return TransactionResult(
            success=True,
            transaction_id=f"0x_refund_{transaction_id[:8]}",
            gateway_provider=self.provider_name,
            amount=amount,
            currency="USD",
            fee_incurred=1.50,
            message=f"Dispatched smart contract refund of ${amount:.2f}."
        )


class CheckoutOrderProcessor:
    """
    High-level checkout coordinator. Operates completely polymorphically:
    it can process orders through ANY PaymentGateway seamlessly!
    """
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def execute_order(self, order_id: str, total_amount: float, customer_info: Dict[str, Any]) -> None:
        print(f"\n[CHECKOUT] Processing Order #{order_id} | Amount: ${total_amount:,.2f}")
        print(f"Selected Payment Provider: {self.gateway.provider_name}")

        result = self.gateway.authorize_and_capture(total_amount, "USD", customer_info)

        if result.success:
            net_revenue = result.amount - result.fee_incurred
            print(f"  [OK] Payment Authorized Successfully!")
            print(f"       Transaction ID: {result.transaction_id}")
            print(f"       Details:        {result.message}")
            print(f"       Merchant Net:   ${net_revenue:,.2f} (Platform Fee: ${result.fee_incurred:.2f})")
        else:
            print(f"  [!] Payment Failed: {result.message}")


# Demonstration of interchangeable gateways:
order_1 = CheckoutOrderProcessor(StripeGateway())
order_1.execute_order("ORD-1001", 249.99, {"card_number": "4111222233339841", "cvc": "123"})

order_2 = CheckoutOrderProcessor(PayPalGateway())
order_2.execute_order("ORD-1002", 79.50, {"paypal_email": "sam.developer@python.org"})

order_3 = CheckoutOrderProcessor(CryptoGateway())
order_3.execute_order("ORD-1003", 1500.00, {"wallet_address": "0x71C836382098a723872938492048203948204928"})

print("\n" + "=" * 75)
print(" ALL 3 PRODUCTION POLYMORPHIC ARCHITECTURES EXECUTED SUCCESSFULLY!")
print("=" * 75)
