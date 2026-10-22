"""Ireland household planner — example figures only."""

from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATE_FMT = "DD/MM/YYYY"

# Indicative Irish OTR-style new prices (EUR). Generic catalogue only — not quotes.
CARS_RAW: list[dict] = [
    {"brand": "Toyota", "name": "Toyota Aygo X", "price_ie": 18_990, "fuel": "petrol", "use": 4.8, "maint": 280, "hold": 1.02},
    {"brand": "Toyota", "name": "Toyota Yaris Hybrid", "price_ie": 28_990, "fuel": "hybrid", "use": 3.8, "maint": 320, "hold": 1.14},
    {"brand": "Toyota", "name": "Toyota Yaris Cross Hybrid", "price_ie": 33_995, "fuel": "hybrid", "use": 4.6, "maint": 340, "hold": 1.15},
    {"brand": "Toyota", "name": "Toyota Corolla Hybrid", "price_ie": 36_450, "fuel": "hybrid", "use": 4.4, "maint": 360, "hold": 1.16},
    {"brand": "Toyota", "name": "Toyota Corolla Touring Sports", "price_ie": 38_450, "fuel": "hybrid", "use": 4.6, "maint": 370, "hold": 1.15},
    {"brand": "Toyota", "name": "Toyota C-HR Hybrid", "price_ie": 39_995, "fuel": "hybrid", "use": 4.8, "maint": 380, "hold": 1.12},
    {"brand": "Toyota", "name": "Toyota C-HR PHEV", "price_ie": 44_990, "fuel": "phev", "use": 5.8, "kwh": 16.5, "ev_range": 66, "maint": 400, "hold": 1.08},
    {"brand": "Toyota", "name": "Toyota Camry Hybrid", "price_ie": 42_990, "fuel": "hybrid", "use": 4.9, "maint": 400, "hold": 1.10},
    {"brand": "Toyota", "name": "Toyota RAV4 Hybrid", "price_ie": 52_495, "fuel": "hybrid", "use": 5.6, "maint": 420, "hold": 1.14},
    {"brand": "Toyota", "name": "Toyota RAV4 PHEV", "price_ie": 54_995, "fuel": "phev", "use": 6.2, "kwh": 18.0, "ev_range": 75, "maint": 430, "hold": 1.10},
    {"brand": "Toyota", "name": "Toyota Highlander Hybrid", "price_ie": 64_995, "fuel": "hybrid", "use": 6.6, "maint": 520, "hold": 1.08},
    {"brand": "Toyota", "name": "Toyota Land Cruiser", "price_ie": 84_995, "fuel": "diesel", "use": 8.5, "maint": 650, "hold": 1.12},
    {"brand": "Toyota", "name": "Toyota Proace Verso", "price_ie": 44_990, "fuel": "diesel", "use": 6.8, "maint": 480, "hold": 1.02},
    {"brand": "Toyota", "name": "Toyota Proace City", "price_ie": 31_990, "fuel": "diesel", "use": 5.4, "maint": 400, "hold": 1.00},
    {"brand": "Toyota", "name": "Toyota Hilux", "price_ie": 44_990, "fuel": "diesel", "use": 7.8, "maint": 520, "hold": 1.10},
    {"brand": "Toyota", "name": "Toyota bZ4X", "price_ie": 47_990, "fuel": "ev", "use": 16.5, "maint": 260, "hold": 0.90},
    {"brand": "Toyota", "name": "Toyota GR Yaris", "price_ie": 52_990, "fuel": "petrol", "use": 8.2, "maint": 550, "hold": 0.95},
    {"brand": "Volkswagen", "name": "VW Polo", "price_ie": 26_990, "fuel": "petrol", "use": 5.4, "maint": 360, "hold": 0.98},
    {"brand": "Volkswagen", "name": "VW Golf", "price_ie": 37_850, "fuel": "petrol", "use": 5.7, "maint": 430, "hold": 0.98},
    {"brand": "Volkswagen", "name": "VW Golf Estate", "price_ie": 39_990, "fuel": "petrol", "use": 5.8, "maint": 440, "hold": 0.97},
    {"brand": "Volkswagen", "name": "VW Golf GTE", "price_ie": 44_990, "fuel": "phev", "use": 5.8, "kwh": 16.0, "ev_range": 80, "maint": 450, "hold": 0.95},
    {"brand": "Volkswagen", "name": "VW T-Cross", "price_ie": 29_990, "fuel": "petrol", "use": 5.6, "maint": 380, "hold": 0.98},
    {"brand": "Volkswagen", "name": "VW Taigo", "price_ie": 31_990, "fuel": "petrol", "use": 5.5, "maint": 380, "hold": 0.97},
    {"brand": "Volkswagen", "name": "VW T-Roc", "price_ie": 35_990, "fuel": "petrol", "use": 6.0, "maint": 410, "hold": 0.98},
    {"brand": "Volkswagen", "name": "VW Tiguan", "price_ie": 47_650, "fuel": "petrol", "use": 6.8, "maint": 480, "hold": 0.97},
    {"brand": "Volkswagen", "name": "VW Tiguan eHybrid", "price_ie": 52_990, "fuel": "phev", "use": 6.9, "kwh": 18.5, "ev_range": 100, "maint": 500, "hold": 0.96},
    {"brand": "Volkswagen", "name": "VW Tiguan Allspace", "price_ie": 49_990, "fuel": "petrol", "use": 7.2, "maint": 500, "hold": 0.96},
    {"brand": "Volkswagen", "name": "VW Passat", "price_ie": 42_990, "fuel": "petrol", "use": 5.9, "maint": 450, "hold": 0.97},
    {"brand": "Volkswagen", "name": "VW Passat eHybrid", "price_ie": 48_990, "fuel": "phev", "use": 6.0, "kwh": 16.8, "ev_range": 90, "maint": 470, "hold": 0.96},
    {"brand": "Volkswagen", "name": "VW Arteon", "price_ie": 49_990, "fuel": "petrol", "use": 6.4, "maint": 520, "hold": 0.94},
    {"brand": "Volkswagen", "name": "VW Touran", "price_ie": 40_990, "fuel": "petrol", "use": 6.5, "maint": 450, "hold": 0.96},
    {"brand": "Volkswagen", "name": "VW ID.3", "price_ie": 41_990, "fuel": "ev", "use": 15.5, "maint": 250, "hold": 0.90},
    {"brand": "Volkswagen", "name": "VW ID.4", "price_ie": 47_990, "fuel": "ev", "use": 16.8, "maint": 260, "hold": 0.91},
    {"brand": "Volkswagen", "name": "VW ID.5", "price_ie": 51_990, "fuel": "ev", "use": 16.6, "maint": 270, "hold": 0.90},
    {"brand": "Volkswagen", "name": "VW ID.7", "price_ie": 54_990, "fuel": "ev", "use": 16.2, "maint": 280, "hold": 0.91},
    {"brand": "Volkswagen", "name": "VW ID. Buzz", "price_ie": 64_990, "fuel": "ev", "use": 19.5, "maint": 320, "hold": 0.92},
    {"brand": "Volkswagen", "name": "VW Caddy", "price_ie": 34_990, "fuel": "diesel", "use": 5.8, "maint": 420, "hold": 1.02},
    {"brand": "Volkswagen", "name": "VW Caddy Maxi", "price_ie": 37_990, "fuel": "diesel", "use": 6.0, "maint": 430, "hold": 1.02},
    {"brand": "Volkswagen", "name": "VW Transporter", "price_ie": 49_995, "fuel": "diesel", "use": 8.1, "maint": 560, "hold": 1.05},
    {"brand": "Volkswagen", "name": "VW Caravelle", "price_ie": 57_990, "fuel": "diesel", "use": 8.3, "maint": 580, "hold": 1.04},
    {"brand": "Volkswagen", "name": "VW Multivan", "price_ie": 62_990, "fuel": "diesel", "use": 7.5, "maint": 590, "hold": 1.00},
    {"brand": "Volkswagen", "name": "VW California", "price_ie": 79_990, "fuel": "diesel", "use": 8.0, "maint": 620, "hold": 1.06},
    {"brand": "Volkswagen", "name": "VW Amarok", "price_ie": 54_990, "fuel": "diesel", "use": 8.4, "maint": 600, "hold": 1.04},
    {"brand": "Volkswagen", "name": "VW Crafter", "price_ie": 52_990, "fuel": "diesel", "use": 8.8, "maint": 580, "hold": 1.00},
    {"brand": "Skoda", "name": "Skoda Fabia", "price_ie": 23_990, "fuel": "petrol", "use": 5.2, "maint": 320, "hold": 1.08},
    {"brand": "Skoda", "name": "Skoda Scala", "price_ie": 26_990, "fuel": "petrol", "use": 5.3, "maint": 340, "hold": 1.08},
    {"brand": "Skoda", "name": "Skoda Octavia", "price_ie": 34_790, "fuel": "petrol", "use": 5.6, "maint": 370, "hold": 1.10},
    {"brand": "Skoda", "name": "Skoda Octavia Estate", "price_ie": 36_490, "fuel": "petrol", "use": 5.7, "maint": 380, "hold": 1.10},
    {"brand": "Skoda", "name": "Skoda Octavia iV", "price_ie": 41_990, "fuel": "phev", "use": 5.8, "kwh": 16.2, "ev_range": 70, "maint": 390, "hold": 1.06},
    {"brand": "Skoda", "name": "Skoda Superb", "price_ie": 41_990, "fuel": "petrol", "use": 6.0, "maint": 400, "hold": 1.08},
    {"brand": "Skoda", "name": "Skoda Superb Estate", "price_ie": 43_490, "fuel": "petrol", "use": 6.1, "maint": 410, "hold": 1.08},
    {"brand": "Skoda", "name": "Skoda Superb iV", "price_ie": 47_990, "fuel": "phev", "use": 6.2, "kwh": 17.0, "ev_range": 80, "maint": 420, "hold": 1.05},
    {"brand": "Skoda", "name": "Skoda Kamiq", "price_ie": 29_990, "fuel": "petrol", "use": 5.5, "maint": 360, "hold": 1.09},
    {"brand": "Skoda", "name": "Skoda Karoq", "price_ie": 34_990, "fuel": "petrol", "use": 6.2, "maint": 390, "hold": 1.09},
    {"brand": "Skoda", "name": "Skoda Kodiaq", "price_ie": 45_990, "fuel": "petrol", "use": 6.9, "maint": 430, "hold": 1.09},
    {"brand": "Skoda", "name": "Skoda Elroq", "price_ie": 41_990, "fuel": "ev", "use": 16.0, "maint": 270, "hold": 0.94},
    {"brand": "Skoda", "name": "Skoda Enyaq", "price_ie": 47_990, "fuel": "ev", "use": 16.4, "maint": 280, "hold": 0.94},
    {"brand": "Skoda", "name": "Skoda Enyaq Coupe", "price_ie": 50_990, "fuel": "ev", "use": 16.2, "maint": 285, "hold": 0.93},
    {"brand": "Other", "name": "Hyundai Tucson Hybrid", "price_ie": 44_995, "fuel": "hybrid", "use": 5.5, "maint": 400, "hold": 1.06},
    {"brand": "Other", "name": "Hyundai Tucson PHEV", "price_ie": 49_990, "fuel": "phev", "use": 6.4, "kwh": 18.0, "ev_range": 62, "maint": 420, "hold": 1.04},
    {"brand": "Other", "name": "Kia Sportage Hybrid", "price_ie": 42_995, "fuel": "hybrid", "use": 5.4, "maint": 390, "hold": 1.08},
    {"brand": "Other", "name": "Kia Sportage PHEV", "price_ie": 48_490, "fuel": "phev", "use": 6.3, "kwh": 17.5, "ev_range": 70, "maint": 410, "hold": 1.05},
    {"brand": "Other", "name": "Nissan Qashqai e-Power", "price_ie": 39_495, "fuel": "hybrid", "use": 5.3, "maint": 410, "hold": 1.02},
    {"brand": "Other", "name": "Ford Puma", "price_ie": 31_995, "fuel": "petrol", "use": 5.8, "maint": 380, "hold": 1.04},
    {"brand": "Other", "name": "Dacia Duster", "price_ie": 26_490, "fuel": "petrol", "use": 6.4, "maint": 320, "hold": 1.00},
    {"brand": "Other", "name": "BMW 3 Series", "price_ie": 54_950, "fuel": "petrol", "use": 6.5, "maint": 720, "hold": 0.94},
    {"brand": "Other", "name": "BMW 330e PHEV", "price_ie": 58_950, "fuel": "phev", "use": 6.4, "kwh": 18.0, "ev_range": 85, "maint": 740, "hold": 0.93},
    {"brand": "Other", "name": "BMW 4 Series", "price_ie": 62_450, "fuel": "petrol", "use": 6.7, "maint": 780, "hold": 0.93},
    {"brand": "Other", "name": "BMW X1", "price_ie": 51_950, "fuel": "petrol", "use": 6.9, "maint": 700, "hold": 0.95},
    {"brand": "Audi", "name": "Audi A1", "price_ie": 32_990, "fuel": "petrol", "use": 5.6, "maint": 520, "hold": 0.97},
    {"brand": "Audi", "name": "Audi A3", "price_ie": 41_750, "fuel": "petrol", "use": 6.1, "maint": 650, "hold": 0.96},
    {"brand": "Audi", "name": "Audi A3 TFSI e", "price_ie": 48_990, "fuel": "phev", "use": 5.9, "kwh": 16.0, "ev_range": 70, "maint": 680, "hold": 0.94},
    {"brand": "Audi", "name": "Audi A4", "price_ie": 49_990, "fuel": "petrol", "use": 6.4, "maint": 720, "hold": 0.95},
    {"brand": "Audi", "name": "Audi A6", "price_ie": 62_990, "fuel": "petrol", "use": 6.8, "maint": 820, "hold": 0.93},
    {"brand": "Audi", "name": "Audi Q2", "price_ie": 38_990, "fuel": "petrol", "use": 6.2, "maint": 620, "hold": 0.96},
    {"brand": "Audi", "name": "Audi Q3", "price_ie": 47_990, "fuel": "petrol", "use": 6.8, "maint": 700, "hold": 0.96},
    {"brand": "Audi", "name": "Audi Q5", "price_ie": 62_490, "fuel": "petrol", "use": 7.4, "maint": 780, "hold": 0.95},
    {"brand": "Audi", "name": "Audi Q4 e-tron", "price_ie": 54_990, "fuel": "ev", "use": 18.2, "maint": 290, "hold": 0.90},
    {"brand": "Audi", "name": "Audi Q8 e-tron", "price_ie": 84_990, "fuel": "ev", "use": 22.0, "maint": 360, "hold": 0.88},
    {"brand": "Renault", "name": "Renault Clio", "price_ie": 23_490, "fuel": "petrol", "use": 5.1, "maint": 310, "hold": 1.02},
    {"brand": "Renault", "name": "Renault Captur", "price_ie": 28_990, "fuel": "petrol", "use": 5.6, "maint": 340, "hold": 1.01},
    {"brand": "Renault", "name": "Renault Austral", "price_ie": 39_990, "fuel": "hybrid", "use": 5.2, "maint": 390, "hold": 1.00},
    {"brand": "Renault", "name": "Renault Arkana", "price_ie": 36_990, "fuel": "hybrid", "use": 5.0, "maint": 380, "hold": 0.99},
    {"brand": "Renault", "name": "Renault Megane E-Tech", "price_ie": 39_990, "fuel": "ev", "use": 15.8, "maint": 250, "hold": 0.92},
    {"brand": "Renault", "name": "Renault Scenic E-Tech", "price_ie": 44_990, "fuel": "ev", "use": 16.8, "maint": 270, "hold": 0.91},
    {"brand": "Renault", "name": "Renault Rafale", "price_ie": 47_990, "fuel": "hybrid", "use": 5.4, "maint": 430, "hold": 0.98},
    {"brand": "Other", "name": "Tesla Model 3", "price_ie": 41_990, "fuel": "ev", "use": 14.5, "maint": 240, "hold": 0.90},
    {"brand": "Other", "name": "Tesla Model Y", "price_ie": 47_990, "fuel": "ev", "use": 16.5, "maint": 260, "hold": 0.91},
    {"brand": "Other", "name": "Hyundai Ioniq 5", "price_ie": 46_995, "fuel": "ev", "use": 16.8, "maint": 280, "hold": 0.92},
    {"brand": "Other", "name": "Kia EV6", "price_ie": 52_495, "fuel": "ev", "use": 16.2, "maint": 290, "hold": 0.93},
]

RUNNING_DEFAULTS = {
    "petrol": {"tax": 190, "ins": 850, "tyres": 480, "service": 280, "kwh": 0.0, "ev_range": 0, "nct": 55},
    "diesel": {"tax": 280, "ins": 920, "tyres": 560, "service": 320, "kwh": 0.0, "ev_range": 0, "nct": 55},
    "hybrid": {"tax": 140, "ins": 820, "tyres": 520, "service": 260, "kwh": 0.0, "ev_range": 0, "nct": 55},
    "phev": {"tax": 90, "ins": 880, "tyres": 560, "service": 310, "kwh": 17.0, "ev_range": 70, "nct": 55},
    "ev": {"tax": 120, "ins": 780, "tyres": 720, "service": 180, "kwh": 16.0, "ev_range": 400, "nct": 55},
}


def enrich_car(raw: dict) -> dict:
    car = dict(raw)
    fuel = car["fuel"]
    defaults = RUNNING_DEFAULTS[fuel]
    for key, value in defaults.items():
        car.setdefault(key, value)
    if fuel == "ev":
        car["kwh"] = car.get("kwh") or car["use"]
        car["ice_use"] = 0.0
    else:
        car["ice_use"] = car["use"]
        car["kwh"] = float(car.get("kwh") or 0.0)
    return car


CARS: list[dict] = [enrich_car(c) for c in CARS_RAW]
BRANDS = ["Toyota", "Volkswagen", "Skoda", "Audi", "Renault", "Other"]

# Indicative Irish dealer / captive-finance averages — not live quotes.
DEALER_FINANCE: dict[str, dict] = {
    "Toyota": {
        "captive": "Toyota Financial Services Ireland",
        "hp_apr": 6.9, "pcp_apr": 5.9, "deposit_pct": 10, "hp_term": 5, "pcp_term": 4, "balloon_pct": 35,
        "note": "TFS typically pushes PCP on hybrids (Yaris/Corolla/RAV4). Campaign APR often 4.9–7.9%; HP a little higher. 4-year PCP balloon commonly ~30–40% of OTR.",
    },
    "Volkswagen": {
        "captive": "Volkswagen Financial Services (Solutions)",
        "hp_apr": 7.5, "pcp_apr": 6.5, "deposit_pct": 10, "hp_term": 5, "pcp_term": 4, "balloon_pct": 38,
        "note": "VWFS Solutions PCP is the volume product on Golf/T-Roc/Tiguan. Headline 5.9–8.9% depending on the campaign. ID. models sometimes get a keener EV rate.",
    },
    "Skoda": {
        "captive": "Škoda Financial Services (VWFS)",
        "hp_apr": 7.2, "pcp_apr": 6.2, "deposit_pct": 10, "hp_term": 5, "pcp_term": 4, "balloon_pct": 36,
        "note": "Same VWFS engine as Volkswagen, often a touch keener on Octavia/Kodiaq. PCP balloons on Enyaq can be optimistic — check the Guaranteed Minimum Future Value.",
    },
    "Audi": {
        "captive": "Audi Financial Services (VWFS)",
        "hp_apr": 8.2, "pcp_apr": 7.3, "deposit_pct": 10, "hp_term": 5, "pcp_term": 4, "balloon_pct": 40,
        "note": "Audi FS tracks VWFS, usually a step above Škoda on the same platform. Q4/Q8 e-tron sometimes get an EV campaign rate.",
    },
    "Renault": {
        "captive": "Renault Finance Ireland",
        "hp_apr": 7.4, "pcp_apr": 6.4, "deposit_pct": 10, "hp_term": 5, "pcp_term": 4, "balloon_pct": 32,
        "note": "Renault Finance is often HP-led on Clio/Captur; E-Tech PCP balloons should be haircut if used EV values look soft.",
    },
    "Other": {
        "captive": "Bank / credit union / broker car loan",
        "hp_apr": 8.9, "pcp_apr": 7.9, "deposit_pct": 15, "hp_term": 5, "pcp_term": 4, "balloon_pct": 30,
        "note": "Without a captive desk, Irish personal car loans often sit ~7.5–11% APR. Credit unions can be cheaper if you qualify.",
    },
}


def dealer_pack(brand: str, model_name: str) -> dict:
    """Brand + model hints for typical Irish dealer finance (indicative)."""
    pack = dict(DEALER_FINANCE.get(brand, DEALER_FINANCE["Other"]))
    name = (model_name or "").lower()
    extras: list[str] = []
    if "bmw" in name:
        pack.update(captive="BMW Financial Services", hp_apr=8.4, pcp_apr=7.5, balloon_pct=40)
        extras.append("BMW FS PCP balloons on 3 Series/X1 are often 35–45%; residual risk sits with you if mileage is high.")
    elif "audi" in name:
        pack.update(captive="Audi Financial Services (VWFS)", hp_apr=8.2, pcp_apr=7.3, balloon_pct=40)
        extras.append("Audi FS tracks VWFS pricing, usually a step above Škoda on the same platform.")
    elif "tesla" in name:
        pack.update(captive="Bank loan / Tesla hire-purchase (limited Irish PCP)", hp_apr=7.8, pcp_apr=7.4, balloon_pct=28, deposit_pct=15)
        extras.append("Tesla Ireland is weaker on classic dealer PCP; many buyers use a credit-union or bank HP instead.")
    elif "hyundai" in name or "kia" in name:
        pack.update(captive="Hyundai/Kia Finance Ireland", hp_apr=6.5, pcp_apr=5.5, balloon_pct=32)
        extras.append("Hyundai/Kia often run the sharpest PCP headlines (sometimes sub-6%) to move Tucson/Sportage/EV6.")
    elif "nissan" in name:
        pack.update(captive="Nissan Financial Services", hp_apr=7.4, pcp_apr=6.4)
        extras.append("Nissan e-Power is often financed like a hybrid PCP; check balloon vs real used values.")
    elif "ford" in name:
        pack.update(captive="Ford Credit", hp_apr=7.6, pcp_apr=6.6)
        extras.append("Ford Credit PCP is common on Puma; deposit 10% keeps the monthly in line with a Golf.")
    elif "dacia" in name:
        pack.update(captive="Dacia Finance (Renault)", hp_apr=7.9, pcp_apr=6.9, deposit_pct=10)
        extras.append("Dacia finance is usually HP-led; the low OTR price matters more than a tiny APR difference.")
    if any(tag in name for tag in ("id.", "enyaq", "elroq", "bz4x", "ioniq", "ev6", "model 3", "model y")):
        extras.append("EV PCP balloons can look cheap monthly but assume a strong residual — haircut the balloon if you doubt the used market.")
        pack["pcp_apr"] = max(pack["pcp_apr"] - 0.4, 4.5)
    if extras:
        pack["note"] = pack["note"] + " " + " ".join(extras)
    return pack

CAR_MARKETS: dict[str, dict] = {
    "Ireland": {
        "price_scale": 1.00, "resale_scale": 1.00, "petrol": 1.72, "diesel": 1.68,
        "electricity": 0.32, "typical_km": 16_000,
        "note": "Irish OTR-style catalogue prices (incl. VRT). Generic estimates, not dealer quotes.",
    },
    "Germany": {
        "price_scale": 0.86, "resale_scale": 0.97, "petrol": 1.74, "diesel": 1.62,
        "electricity": 0.33, "typical_km": 14_000,
        "note": "German list prices are usually below Irish OTR because there is no VRT.",
    },
    "Belgium": {
        "price_scale": 0.90, "resale_scale": 0.98, "petrol": 1.75, "diesel": 1.78,
        "electricity": 0.35, "typical_km": 15_000,
        "note": "Belgian on-the-road levels scaled from the Irish baseline.",
    },
    "United Kingdom": {
        "price_scale": 0.88, "resale_scale": 1.02, "petrol": 1.62, "diesel": 1.67,
        "electricity": 0.30, "typical_km": 12_000,
        "note": "UK prices expressed in euro-equivalent OTR levels.",
    },
    "France": {
        "price_scale": 0.88, "resale_scale": 0.96, "petrol": 1.78, "diesel": 1.70,
        "electricity": 0.27, "typical_km": 13_000,
        "note": "French list prices scaled from the Irish baseline.",
    },
    "Netherlands": {
        "price_scale": 0.94, "resale_scale": 0.98, "petrol": 2.05, "diesel": 1.85,
        "electricity": 0.30, "typical_km": 14_000,
        "note": "Dutch prices and high petrol duty, scaled from the Irish baseline.",
    },
}

# Indicative Irish owner-occupier fixed rates by lender, deposit (LTV) and term. Not live quotes.
IRISH_BANKS: list[dict] = [
    {"bank": "AIB", "ltv": {10: {20: 4.35, 30: 4.15, 35: 4.05}, 20: {20: 3.95, 30: 3.75, 35: 3.65}, 30: {20: 3.75, 30: 3.55, 35: 3.45}}},
    {"bank": "Bank of Ireland", "ltv": {10: {20: 4.45, 30: 4.25, 35: 4.15}, 20: {20: 4.05, 30: 3.85, 35: 3.75}, 30: {20: 3.85, 30: 3.65, 35: 3.55}}},
    {"bank": "Permanent TSB", "ltv": {10: {20: 4.55, 30: 4.35, 35: 4.25}, 20: {20: 4.15, 30: 3.95, 35: 3.85}, 30: {20: 3.95, 30: 3.75, 35: 3.65}}},
    {"bank": "EBS", "ltv": {10: {20: 4.40, 30: 4.20, 35: 4.10}, 20: {20: 4.00, 30: 3.80, 35: 3.70}, 30: {20: 3.80, 30: 3.60, 35: 3.50}}},
    {"bank": "Haven (brokers)", "ltv": {10: {20: 4.30, 30: 4.10, 35: 4.00}, 20: {20: 3.90, 30: 3.70, 35: 3.60}, 30: {20: 3.70, 30: 3.50, 35: 3.40}}},
]

# Investment / BTL Irish rates are typically 1.2–2.0pp above owner-occupier.
IRISH_BTL: list[dict] = [
    {"lender": "AIB (ICS / BTL)", "ltv30": 5.35, "ltv40": 5.15, "note": "Often 30%+ deposit. Rate usually 1.3–1.8pp over owner-occ."},
    {"lender": "Bank of Ireland BTL", "ltv30": 5.55, "ltv40": 5.35, "note": "Limited BTL book; stress-test rental cover tightly."},
    {"lender": "Permanent TSB BTL", "ltv30": 5.65, "ltv40": 5.45, "note": "Common broker route. Watch arrangement fees."},
    {"lender": "Non-bank / specialist", "ltv30": 6.25, "ltv40": 5.95, "note": "Finance Ireland-style: quicker, dearer, more fees."},
]

MORTGAGE_MARKETS: dict[str, dict] = {
    "Ireland": {
        "rates": {10: 4.25, 20: 3.80, 30: 3.55}, "stamp": 0.01,
        "note": "Indicative Irish fixed-rate brackets. 10% deposit is the dearest LTV; 20% is the volume band; 30% is closer to high-equity pricing. Stamp duty simplified at 1% (home).",
    },
    "Germany": {
        "rates": {10: 3.70, 20: 3.35, 30: 3.15}, "stamp": 0.065,
        "note": "Indicative German brackets ~3.2–3.7%. Purchase tax simplified at 6.5%.",
    },
    "Belgium": {
        "rates": {10: 3.85, 20: 3.50, 30: 3.30}, "stamp": 0.03,
        "note": "Indicative Belgian brackets ~3.3–3.9%. Registration duty simplified at 3%.",
    },
}

st.set_page_config(page_title="Ireland Household Planner", page_icon="💹", layout="wide")

st.sidebar.header("Go to a section")
st.sidebar.caption("The large tab bar under the master graph matches this list. Pick a tab any time — it stays on the page.")
st.sidebar.markdown(
    "- **Master** — cash, net worth, explainer\n"
    "- **Snapshot** — every major chart\n"
    "- **Earners** — pay, tax, pension\n"
    "- **Housing** — mortgage, banks, home\n"
    "- **Investments** — sleeves and tax\n"
    "- **Ventures** — business / rental\n"
    "- **Automotive TCO** — cars\n"
    "- **Family & Education**\n"
    "- **Lifestyle** — including medical"
)
st.sidebar.radio(
    "Put graphs",
    ["Beside inputs", "Below inputs", "Wide"],
    key="chart_place",
    help="Beside = inputs left, chart right. Below = stacked. Wide = full-width chart.",
)

st.sidebar.header("Display currency")
currency_label = st.sidebar.radio("View figures in", ["Euro (€)", "US dollar ($)"], index=0)
eur_usd = st.sidebar.number_input(
    "EUR → USD rate", min_value=0.50, max_value=2.00, value=1.08, step=0.01, format="%.2f",
    help="Used only when viewing in US dollars. All inputs stay in euro.",
)
is_eur = currency_label.startswith("Euro")
cur = "€" if is_eur else "$"
tick = ",.2f"
MONEY_FMT = "%.2f"
SMALL_BENEFIT_CAP = 1_000.0


def to_display(eur_value: float) -> float:
    return float(eur_value) if is_eur else float(eur_value) * eur_usd


def comma(value: float, decimals: int = 0) -> str:
    """Non-currency counts (years, km, people). Cash uses money() with two decimals."""
    n = float(value)
    return f"{n:,.{decimals}f}"


def money(eur_value: float, decimals: int = 2) -> str:
    return f"{cur}{comma(to_display(eur_value), decimals)}"


SNAPSHOT_FIGS: list[tuple[str, object]] = []
AXIS_MONEY = dict(
    tickformat=",.2f",
    tickprefix=f"{cur}",
    separatethousands=True,
    hoverformat=",.2f",
    exponentformat="none",
    tickfont=dict(size=12),
    nticks=12,
    automargin=True,
    showgrid=True,
    gridwidth=1,
    griddash="dot",
    zeroline=True,
    zerolinewidth=1,
)


def irish_bank_rate(bank: str, deposit_pct: int, term: int) -> float:
    row = next((b for b in IRISH_BANKS if b["bank"] == bank), IRISH_BANKS[0])
    ltv = min(row["ltv"], key=lambda x: abs(x - int(deposit_pct)))
    terms = row["ltv"][ltv]
    nearest_term = min(terms, key=lambda x: abs(x - int(term)))
    return float(terms[nearest_term])


def format_money_fig(fig):
    """Force €1,234.56 on every cash axis — no raw floats, no 1e6 notation."""
    fig.update_layout(separators=".,", font=dict(size=13))
    fig.update_yaxes(**AXIS_MONEY)
    fig.update_xaxes(
        showgrid=True, gridwidth=1, griddash="dot", automargin=True, nticks=12,
        separatethousands=False, tickformat="d",
    )
    fig.update_layout(
        yaxis_tickformat=",.2f", yaxis_tickprefix=cur, yaxis_exponentformat="none",
        yaxis_separatethousands=True, yaxis_hoverformat=",.2f",
        xaxis_separatethousands=False,
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="left", x=0, font=dict(size=11)),
        margin=dict(l=80, r=70, t=70, b=110),
    )
    if any(getattr(tr, "yaxis", None) == "y2" for tr in fig.data):
        title = None
        if fig.layout.yaxis2 and fig.layout.yaxis2.title:
            title = fig.layout.yaxis2.title.text or fig.layout.yaxis2.title
        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                title=str(title or "Pension pots"),
                tickformat=",.2f",
                tickprefix=cur,
                separatethousands=True,
                hoverformat=",.2f",
                exponentformat="none",
                tickfont=dict(size=12),
                nticks=12,
                automargin=True,
                showgrid=False,
            )
        )
    for tr in fig.data:
        if getattr(tr, "type", None) in ("bar", "scatter"):
            tr.hovertemplate = f"{cur}%{{y:,.2f}}<extra>%{{fullData.name}}</extra>"
    return fig


def plot_money(fig, snap: str | None = None) -> None:
    format_money_fig(fig)
    if snap:
        SNAPSHOT_FIGS.append((snap, fig))
    st.plotly_chart(fig, width="stretch")


def add_plan_markers(fig, start_year: int, retire_year: int | None, start_cash: float | None = None) -> None:
    fig.add_vline(
        x=start_year, line_dash="dot", line_color="#54A24B", line_width=1,
        annotation_text=f"Start · cash {money(start_cash)}" if start_cash is not None else "Start",
        annotation_position="top left",
    )
    if retire_year and retire_year <= start_year + time_horizon_years:
        fig.add_vline(
            x=retire_year, line_dash="dash", line_color="#F58518", line_width=2,
            annotation_text=f"Retirement ({retirement_age}) · drawdown",
            annotation_position="top",
        )


def irish_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def explainer_scroll(md: str, height: int = 280) -> None:
    """Fixed-height scroll box with explicit dark-on-light text (theme-proof)."""
    import html as htmlmod
    import re

    body = htmlmod.escape(md)
    body = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", body)
    parts: list[str] = []
    in_list = False
    for raw in body.split("\n"):
        line = raw.strip()
        if line.startswith("- "):
            if not in_list:
                parts.append("<ul style='margin:0.35rem 0 0.7rem 1.15rem;padding:0;color:#1a1a1a;'>")
                in_list = True
            parts.append(f"<li style='margin:0.28rem 0;color:#1a1a1a;'>{line[2:]}</li>")
            continue
        if in_list:
            parts.append("</ul>")
            in_list = False
        if not line:
            continue
        if line.startswith("<strong>") and line.endswith("</strong>") and line.count("<strong>") == 1:
            parts.append(
                f"<div style='margin-top:0.65rem;font-weight:700;color:#111111;'>{line}</div>"
            )
        else:
            parts.append(f"<p style='margin:0.35rem 0;color:#1a1a1a;'>{line}</p>")
    if in_list:
        parts.append("</ul>")
    box = (
        f"<div style='height:{height}px;overflow-y:auto;overflow-x:hidden;padding:10px 12px;"
        "border:1px solid #c8c4bb;border-radius:8px;background:#f7f4ec;color:#1a1a1a;"
        "font-family:sans-serif;font-size:0.92rem;line-height:1.45;'>"
        f"{''.join(parts)}</div>"
    )
    st.components.v1.html(box, height=height + 16, scrolling=False)


def note(text: str) -> None:
    """Footnote under a control: typical Irish/EU bands, not a quote."""
    st.caption(text)


def advice_box(title: str, bullets: list[str]) -> None:
    md = "**" + title + "**\n\n" + "\n\n".join(f"- {b}" for b in bullets)
    explainer_scroll(md, height=280)


def graph_pair():
    """Return (input_col, chart_col) or (None, None) if stacked/wide."""
    mode = str(st.session_state.get("chart_place", "Beside inputs"))
    if mode.startswith("Beside"):
        return st.columns([1, 1.35], vertical_alignment="top")
    return None, None


def date_field(label: str, value: date, key: str | None = None, **kwargs):
    return st.date_input(label, value=value, format=DATE_FMT, key=key, **kwargs)


def banded_euro(label: str, bands: dict, default: str, footnote: str, key: str, custom: float) -> float:
    """Select a typical Irish cost band; defaults to the named average, with a custom override."""
    options = list(bands.keys())
    choice = st.selectbox(label, options, index=options.index(default), key=key)
    note(footnote)
    raw = bands[choice]
    if raw is None:
        return st.number_input(
            f"Custom — {label} (€ / year)", min_value=0.0, value=float(custom),
            step=100.0, format=MONEY_FMT, key=f"{key}_custom",
        )
    st.caption(f"Using {money(raw)} / year. Pick another band or Custom to change it.")
    return float(raw)


def age_months(as_of: date, birth: date) -> int:
    return (as_of.year - birth.year) * 12 + as_of.month - birth.month


CHILDCARE_BANDS = {
    "Part-time creche (~€650)": 650.0,
    "Full-time, outside Dublin (~€950)": 950.0,
    "Full-time, Dublin (~€1,250)": 1_250.0,
    "Childminder / nanny share (~€850)": 850.0,
    "Custom amount": None,
}
CHILD_COST_BANDS = {
    "Lean clothes + school (~€2,400)": 2_400.0,
    "Typical clothes, school, activities (~€4,500)": 4_500.0,
    "Older kids / lots of activities (~€7,000)": 7_000.0,
    "Custom amount": None,
}
UNI_FEE_BANDS = {
    "Irish student contribution (~€3,000)": 3_000.0,
    "Irish + materials / field trips (~€3,800)": 3_800.0,
    "UK / EU fees (~€10,000)": 10_000.0,
    "Non-EU / US-style (~€25,000)": 25_000.0,
    "Custom amount": None,
}
UNI_RENT_BANDS = {
    "Shared house, regional (~€5,400)": 5_400.0,
    "Away from home, typical (~€7,200)": 7_200.0,
    "Dublin / high-rent (~€10,800)": 10_800.0,
    "Custom amount": None,
}
UNI_POCKET_BANDS = {
    "Lean (~€2,400)": 2_400.0,
    "Typical student (~€3,600)": 3_600.0,
    "Comfortable (~€5,400)": 5_400.0,
    "Custom amount": None,
}
POST_COLLEGE_BANDS = {
    "None — they cover themselves (€0)": 0.0,
    "Light help (~€4,000)": 4_000.0,
    "Help with rent while starting work (~€7,200)": 7_200.0,
    "Custom amount": None,
}


st.sidebar.divider()
st.sidebar.header("Planning dates")
planning_start = st.sidebar.date_input("Planning start date", value=date.today(), format=DATE_FMT)
if "master_horizon" not in st.session_state:
    st.session_state.master_horizon = 55
if "retirement_age" not in st.session_state:
    st.session_state.retirement_age = 66
if "include_business" not in st.session_state:
    st.session_state.include_business = False
if "include_rental" not in st.session_state:
    st.session_state.include_rental = False
if "include_starting_cash" not in st.session_state:
    st.session_state.include_starting_cash = True
if "initial_cash" not in st.session_state:
    st.session_state.initial_cash = 10_000.0
if "existing_investments" not in st.session_state:
    st.session_state.existing_investments = 0.0
if "chart_place" not in st.session_state:
    st.session_state.chart_place = "Beside inputs"
time_horizon_years = int(st.session_state.master_horizon)
retirement_age = int(st.session_state.retirement_age)
include_business = bool(st.session_state.include_business)
include_rental = bool(st.session_state.include_rental)
include_starting_cash = bool(st.session_state.include_starting_cash)
st.sidebar.caption(
    f"Timeframe and retirement age sit under the master graph. "
    f"Now: {comma(time_horizon_years)}y horizon, retire at {comma(retirement_age)} (Irish State Pension age is 66)."
)
STATE_PENSION = 14_420.0  # ~max contributory, weekly × 52, taxable, indicative

st.sidebar.divider()
st.sidebar.header("Global parameters")
st.sidebar.caption("Starter figures are round examples. Starting cash is the amount box above the master graph.")

initial_cash = float(st.session_state.initial_cash)
plan_start_cash = initial_cash if include_starting_cash else 0.0
monthly_investments = st.sidebar.number_input("Monthly investments (€)", min_value=0.0, value=250.0, step=50.0, format="%.2f")
mortgage_balance = st.sidebar.number_input("Mortgage balance (€)", min_value=0.0, value=250_000.0, step=5_000.0, format="%.2f")
home_value = st.sidebar.number_input("Home value (€)", min_value=0.0, value=350_000.0, step=5_000.0, format="%.2f")
annual_return = st.sidebar.slider("Assumed investment return (annual %)", 0.0, 15.0, 6.0, 0.1)
mortgage_rate = st.sidebar.slider("Assumed mortgage rate (annual %)", 0.0, 12.0, 4.0, 0.1)
monthly_mortgage_payment = st.sidebar.number_input(
    "Monthly mortgage payment (€)", min_value=0.0, value=1_200.0, step=50.0, format="%.2f"
)


def project_finances(
    cash: float, monthly_contrib: float, home: float, mortgage: float, years: int,
    invest_return: float, loan_rate: float, monthly_payment: float,
    start_investments: float = 0.0,
) -> pd.DataFrame:
    months = years * 12
    r_invest = (1 + invest_return / 100) ** (1 / 12) - 1
    r_loan = loan_rate / 100 / 12
    records: list[dict[str, float]] = []
    investments = float(start_investments)
    remaining_mortgage = mortgage
    for m in range(months + 1):
        liquid = investments
        illiquid = home
        assets = cash + liquid + illiquid
        records.append(
            {
                "month": m, "year": m / 12, "cash": cash, "investments": investments,
                "home_value": home, "liquid_assets": liquid, "illiquid_assets": illiquid,
                "total_assets": assets, "total_liabilities": remaining_mortgage,
                "mortgage_balance": remaining_mortgage, "net_worth": assets - remaining_mortgage,
            }
        )
        if m == months:
            break
        investments = investments * (1 + r_invest) + monthly_contrib
        interest = remaining_mortgage * r_loan
        principal = min(max(monthly_payment - interest, 0.0), remaining_mortgage)
        remaining_mortgage = max(remaining_mortgage - principal, 0.0)
    return pd.DataFrame(records)


def annual_depreciation_rate(year: int, hold: float, annual_km: float, typical_km: float) -> float:
    if year == 1:
        base = 0.21
    elif year == 2:
        base = 0.14
    elif year == 3:
        base = 0.11
    else:
        base = max(0.05, 0.08 - 0.004 * (year - 4))
    brand = base / max(hold, 0.75)
    mileage = 1 + max(-0.08, min(0.28, (annual_km - typical_km) / 80_000))
    return min(0.38, brand * mileage)


def phev_utility_factor(ev_range: float, annual_km: float) -> float:
    """Share of km likely done on electric, given daily mileage vs plug-in range."""
    if ev_range <= 0 or annual_km <= 0:
        return 0.0
    daily = annual_km / 365
    return float(min(0.90, ev_range / max(daily, 1.0) * 0.72))


def energy_cost(car: dict, market: dict, annual_km: float) -> tuple[float, float, float]:
    """Return (petrol/diesel €, electricity €, electric km share)."""
    fuel = car["fuel"]
    petrol_p = market["diesel"] if fuel == "diesel" else market["petrol"]
    elec_p = market["electricity"]
    if fuel == "ev":
        return 0.0, annual_km * car["kwh"] / 100 * elec_p, 1.0
    if fuel == "phev":
        uf = phev_utility_factor(car["ev_range"], annual_km)
        elec_km = annual_km * uf
        ice_km = annual_km - elec_km
        petrol = ice_km * car["ice_use"] / 100 * petrol_p
        electricity = elec_km * car["kwh"] / 100 * elec_p
        return petrol, electricity, uf
    return annual_km * car["ice_use"] / 100 * petrol_p, 0.0, 0.0


def nct_due(year: int) -> bool:
    """Irish passenger NCT: first test in year 4, then every 2 years."""
    return year >= 4 and (year - 4) % 2 == 0


def project_vehicle_tco(car: dict, market: dict, years: int, annual_km: float) -> pd.DataFrame:
    scale = market["price_scale"]
    purchase = car["price_ie"] * scale
    remaining = purchase
    rows: list[dict] = []
    totals = {k: 0.0 for k in ("maint", "energy", "petrol", "electricity", "tyres", "service", "nct", "tax", "insurance")}
    age_factor = 0.07 if car["fuel"] == "ev" else 0.12
    petrol, electricity, uf = energy_cost(car, market, annual_km)
    energy = petrol + electricity
    tyres = car["tyres"] * scale * (annual_km / 40_000)
    for year in range(1, max(years, 1) + 1):
        rate = annual_depreciation_rate(year, car["hold"], annual_km, market["typical_km"])
        drop = remaining * rate
        remaining -= drop
        remaining *= market["resale_scale"] if year == years else 1.0
        remaining = max(purchase * 0.12, remaining)
        service = car["service"] * scale * (1 + age_factor * (year - 1))
        repairs = car["maint"] * scale * (1 + age_factor * (year - 1)) * (annual_km / market["typical_km"])
        nct = car["nct"] * scale if nct_due(year) else 0.0
        tax = car["tax"] * scale
        insurance = car["ins"] * scale * (1 + 0.02 * (year - 1))
        standing = tyres + service + nct + tax + insurance + repairs
        for key, val in (
            ("maint", repairs), ("energy", energy), ("petrol", petrol), ("electricity", electricity),
            ("tyres", tyres), ("service", service), ("nct", nct), ("tax", tax), ("insurance", insurance),
        ):
            totals[key] += val
        running = standing + energy
        rows.append(
            {
                "year": year, "purchase": purchase, "value": remaining, "depreciation": drop,
                "cum_depreciation": purchase - remaining, "maintenance": repairs,
                "cum_maintenance": totals["maint"], "energy": energy, "petrol": petrol,
                "electricity": electricity, "cum_energy": totals["energy"], "tyres": tyres,
                "service": service, "nct": nct, "tax": tax, "insurance": insurance,
                "standing": standing, "ev_share": uf, "resale": remaining,
                "net_tco": purchase + totals["maint"] + totals["energy"] + totals["tyres"]
                + totals["service"] + totals["nct"] + totals["tax"] + totals["insurance"] - remaining,
                "running": running,
            }
        )
    return pd.DataFrame(rows)


def standard_payment(principal: float, annual_rate: float, years: int) -> float:
    n = years * 12
    r = annual_rate / 100 / 12
    if n <= 0:
        return 0.0
    if r == 0:
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def amortize(principal: float, annual_rate: float, years: int, extra_monthly: float = 0.0) -> pd.DataFrame:
    payment = standard_payment(principal, annual_rate, years)
    r = annual_rate / 100 / 12
    max_months = years * 12
    bal = principal
    total_interest = 0.0
    total_principal = 0.0
    year_interest = 0.0
    year_principal = 0.0
    rows: list[dict] = []
    for month in range(1, max_months + 1):
        if bal <= 0.5:
            break
        interest = bal * r
        principal_pay = min(max(payment - interest, 0.0) + extra_monthly, bal)
        bal = max(bal - principal_pay, 0.0)
        total_interest += interest
        total_principal += principal_pay
        year_interest += interest
        year_principal += principal_pay
        if month % 12 == 0 or bal <= 0.5 or month == max_months:
            rows.append(
                {
                    "month": month, "year": (month + 11) // 12, "payment": payment,
                    "interest": year_interest, "principal": year_principal, "balance": bal,
                    "cum_interest": total_interest, "cum_principal": total_principal,
                }
            )
            year_interest = 0.0
            year_principal = 0.0
    return pd.DataFrame(rows)


def project_ucits_etf(
    initial: float, monthly: float, years: int, gross_return: float,
    exit_tax: float = 0.41, deemed_years: int = 8, liquidate_at_end: bool = True,
) -> pd.DataFrame:
    r_m = (1 + gross_return / 100) ** (1 / 12) - 1
    value = initial
    basis = initial
    tax_paid = 0.0
    rows: list[dict] = []
    months = years * 12
    for m in range(1, months + 1):
        value = value * (1 + r_m) + monthly
        basis += monthly
        deemed = m % (deemed_years * 12) == 0
        if deemed:
            gain = max(value - basis, 0.0)
            tax = gain * exit_tax
            value -= tax
            basis = value
            tax_paid += tax
        if m % 12 == 0:
            rows.append({
                "year": m / 12, "net_value": value, "basis": basis, "tax_paid": tax_paid,
                "deemed": deemed, "contributed": initial + monthly * m,
            })
    if liquidate_at_end and months > 0 and value > basis:
        tax = (value - basis) * exit_tax
        value -= tax
        tax_paid += tax
        if rows:
            rows[-1]["net_value"] = value
            rows[-1]["tax_paid"] = tax_paid
            rows[-1]["basis"] = value
    return pd.DataFrame(rows)


def project_dividend_kings(
    initial: float, monthly: float, years: int, price_growth: float, dividend_yield: float,
    dividend_tax: float = 0.33, cgt: float = 0.33,
) -> pd.DataFrame:
    r_m = (1 + price_growth / 100) ** (1 / 12) - 1
    y_m = dividend_yield / 100 / 12
    value = initial
    basis = initial
    tax_paid = 0.0
    rows: list[dict] = []
    months = years * 12
    for m in range(1, months + 1):
        value = value * (1 + r_m) + monthly
        basis += monthly
        dividend = value * y_m
        tax = dividend * dividend_tax
        net_div = dividend - tax
        value += net_div
        basis += net_div
        tax_paid += tax
        if m % 12 == 0:
            latent_cgt = max(value - basis, 0.0) * cgt
            rows.append(
                {
                    "year": m / 12, "net_value": value - latent_cgt, "pre_cgt": value,
                    "basis": basis, "tax_paid": tax_paid + latent_cgt, "div_tax": tax_paid,
                    "contributed": initial + monthly * m,
                }
            )
    return pd.DataFrame(rows)


def irish_usc(gross: float) -> float:
    """Indicative PAYE USC (not a Revenue calculator)."""
    bands = [(12_012, 0.005), (27_382, 0.02), (70_044, 0.04), (float("inf"), 0.08)]
    tax = 0.0
    lower = 0.0
    remaining = max(gross, 0.0)
    for upper, rate in bands:
        slice_amt = min(remaining, upper - lower)
        if slice_amt <= 0:
            break
        tax += slice_amt * rate
        remaining -= slice_amt
        lower = upper
        if remaining <= 0:
            break
    return tax


def irish_income_tax(taxable: float, credits: float = 3_750.0) -> float:
    """Single-person 20%/40% with standard PAYE+personal credits (indicative)."""
    band = 44_000.0
    tax = min(taxable, band) * 0.20 + max(taxable - band, 0.0) * 0.40
    return max(tax - credits, 0.0)


def irish_paye(
    gross: float, employee_pension: float, bik: float = 0.0, tax_free_cash: float = 0.0,
) -> dict[str, float]:
    """PAYE pack: tax on cash emoluments + BIK; tax-free cash is added after tax."""
    pension = min(max(employee_pension, 0.0), max(gross, 0.0))
    emoluments = max(gross, 0.0) + max(bik, 0.0)
    taxable = max(emoluments - pension, 0.0)
    income_tax = irish_income_tax(taxable)
    usc = irish_usc(emoluments)
    prsi = taxable * 0.041
    net = gross - pension - income_tax - usc - prsi + max(tax_free_cash, 0.0)
    return {
        "gross": gross, "pension": pension, "taxable": taxable, "bik": max(bik, 0.0),
        "tax_free": max(tax_free_cash, 0.0), "emoluments": emoluments,
        "income_tax": income_tax, "usc": usc, "prsi": prsi, "net": max(net, 0.0),
        "effective": (income_tax + usc + prsi) / emoluments if emoluments else 0.0,
        "marginal": 0.52 if taxable > 44_000 else 0.28,
    }


def pension_age_limit_pct(age: int) -> float:
    if age < 30:
        return 0.15
    if age < 40:
        return 0.20
    if age < 50:
        return 0.25
    if age < 55:
        return 0.30
    if age < 60:
        return 0.35
    return 0.40


def project_equity_sleeve(
    initial: float, monthly: float, years: int, price_growth: float, dividend_yield: float,
    dividend_tax: float = 0.33, cgt: float = 0.33,
) -> pd.DataFrame:
    """Direct shares: 33% DWT/income on dividends, 33% CGT reserved on gains."""
    return project_dividend_kings(
        initial, monthly, years, price_growth, dividend_yield, dividend_tax, cgt
    )


def age_on(as_of: date, birth: date) -> int:
    years = as_of.year - birth.year
    if (as_of.month, as_of.day) < (birth.month, birth.day):
        years -= 1
    return years


def childcare_months_in_year(year: int, birth: date, leave_months: int, until_age: int) -> int:
    """Months in this calendar year after parental leave and before school-age cutoff."""
    count = 0
    for month in range(1, 13):
        as_of = date(year, month, 28)
        if as_of < birth:
            continue
        age_m = age_months(as_of, birth)
        if age_m >= leave_months and age_m < until_age * 12:
            count += 1
    return count


def family_timeline(
    start: date, years: int, children: list[dict], childcare_until: int,
    childcare_monthly: float, child_annual: float, child_until: int, uni_years: int,
    uni_fees: float, uni_rent: float, uni_pocket: float,
    support_annual: float, support_years: int,
) -> pd.DataFrame:
    rows: list[dict] = []
    cum = 0.0
    for offset in range(years):
        as_of = date(start.year + offset, start.month, min(start.day, 28))
        year = start.year + offset
        childcare = kids = fees = rent = pocket = support = 0.0
        for child in children:
            age = age_on(as_of, child["birth"])
            if 0 <= age < child_until:
                kids += child_annual
            paid_months = childcare_months_in_year(
                year, child["birth"], child.get("leave_months", 0), childcare_until
            )
            childcare += childcare_monthly * paid_months
            if child["college"]:
                uni_start = child["college_start"]
                uni_end = date(uni_start.year + uni_years, uni_start.month, min(uni_start.day, 28))
                if uni_start <= as_of < uni_end:
                    fees += uni_fees
                    if child.get("lives_away"):
                        rent += uni_rent
                    pocket += uni_pocket
                if child.get("post_college") and support_annual > 0 and support_years > 0:
                    post_end = date(uni_end.year + support_years, uni_end.month, min(uni_end.day, 28))
                    if uni_end <= as_of < post_end:
                        support += support_annual
        uni = fees + rent + pocket
        total = childcare + kids + uni + support
        cum += total
        rows.append(
            {
                "year": as_of.year, "childcare": childcare, "child_costs": kids,
                "uni_fees": fees, "uni_rent": rent, "uni_pocket": pocket,
                "university": uni, "post_college": support, "total": total, "cumulative": cum,
            }
        )
    return pd.DataFrame(rows)


def col_year(df: pd.DataFrame | None, year: int, column: str, year_col: str = "year") -> float:
    if df is None or df.empty or column not in df.columns or year_col not in df.columns:
        return 0.0
    hit = df.loc[df[year_col] == year, column]
    return float(hit.sum()) if len(hit) else 0.0


def fleet_timeline(slots: list[dict], market: dict, start: date, horizon_years: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    end_year = start.year + horizon_years
    years = list(range(start.year, end_year + 1))
    cols = [
        "depreciation", "maintenance", "energy", "tyres", "service", "nct", "tax", "insurance",
        "capex_net", "cash_capex", "finance_pay", "loan_end",
    ]
    cal = pd.DataFrame({"calendar_year": years, **{c: 0.0 for c in cols}}).set_index("calendar_year")
    summaries: list[dict] = []
    for slot in slots:
        car, km = slot["car"], slot["km"]
        replace_every = max(int(slot["replace_years"]), 1)
        buy = slot["buy_date"]
        mode = slot.get("finance", "Hire purchase (HP)")
        apr = float(slot.get("apr", 7.0))
        dep_pct = float(slot.get("deposit_pct", 10))
        term = max(int(slot.get("term", 5)), 1)
        balloon_pct = float(slot.get("balloon_pct", 0))
        cycle = 0
        cycle_start = buy
        slot_tco = 0.0
        residual = 0.0
        monthly_show = 0.0
        while cycle_start.year <= end_year:
            remaining = end_year - cycle_start.year
            if remaining < 1:
                break
            own = min(replace_every, remaining)
            tco = project_vehicle_tco(car, market, own, km)
            sells = own == replace_every and (cycle_start.year + own) <= end_year
            purchase = float(tco["purchase"].iloc[0])
            resale = float(tco["resale"].iloc[-1])
            for _, row in tco.iterrows():
                yr = cycle_start.year + int(row["year"]) - 1
                if yr in cal.index:
                    for col in ("depreciation", "maintenance", "energy", "tyres", "service", "nct", "tax", "insurance"):
                        cal.loc[yr, col] += row[col]
            if cycle_start.year in cal.index:
                cal.loc[cycle_start.year, "capex_net"] += purchase
            if sells and (cycle_start.year + own) in cal.index:
                cal.loc[cycle_start.year + own, "capex_net"] -= resale

            cash_buy = mode.startswith("Cash")
            pcp = "PCP" in mode
            deposit = 0.0 if cash_buy else purchase * dep_pct / 100
            balloon = purchase * balloon_pct / 100 if pcp and not cash_buy else 0.0
            loan = 0.0 if cash_buy else max(purchase - deposit - balloon, 0.0)
            term_use = min(term, own)
            if cash_buy and cycle_start.year in cal.index:
                cal.loc[cycle_start.year, "cash_capex"] += purchase
            elif cycle_start.year in cal.index:
                cal.loc[cycle_start.year, "cash_capex"] += deposit
            payoff = 0.0
            if loan > 0 and term_use > 0:
                sched = amortize(loan, apr, term_use, 0.0)
                monthly_show = standard_payment(loan, apr, term_use)
                for _, srow in sched.iterrows():
                    yr = cycle_start.year + int(srow["year"]) - 1
                    if yr in cal.index:
                        cal.loc[yr, "finance_pay"] += float(srow["interest"] + srow["principal"])
                        cal.loc[yr, "loan_end"] += float(srow["balance"])
                last_bal_year = cycle_start.year + term_use - 1
                if not sched.empty:
                    payoff = float(sched["balance"].iloc[-1])
                    if last_bal_year in cal.index and payoff < 1:
                        payoff = 0.0
            if pcp:
                for age in range(term_use):
                    yr = cycle_start.year + age
                    if yr in cal.index:
                        cal.loc[yr, "loan_end"] += balloon
                payoff += balloon
                end_y = cycle_start.year + term_use
                if end_y in cal.index and not sells:
                    cal.loc[end_y, "cash_capex"] += balloon
                    payoff = 0.0
            settle_y = cycle_start.year + own
            if sells and settle_y in cal.index:
                cal.loc[settle_y, "cash_capex"] -= (resale - payoff)
            elif not sells:
                residual = resale

            slot_tco += float(tco["net_tco"].iloc[-1]) + (0.0 if sells else resale)
            slot_tco -= resale if sells else 0.0
            residual = 0.0 if sells else resale
            cycle += 1
            cycle_start = date(cycle_start.year + replace_every, cycle_start.month, min(cycle_start.day, 28))
        summaries.append(
            {
                "Vehicle": slot["label"], "Model": car["name"], "Fuel": car["fuel"].upper(),
                "Finance": mode, "APR": f"{apr:.1f}%",
                "First purchase": irish_date(buy), "Replace every": f"{replace_every}y",
                "Monthly (indicative)": monthly_show,
                "Cycles": comma(cycle), "Horizon TCO": slot_tco, "Residual at horizon": residual,
            }
        )
    cal = cal.reset_index()
    cal["standing"] = cal["tyres"] + cal["service"] + cal["nct"] + cal["tax"] + cal["insurance"]
    cal["running"] = cal["depreciation"] + cal["maintenance"] + cal["energy"] + cal["standing"]
    cal["total"] = cal["running"] + cal["capex_net"]
    cal["cash_cars"] = cal["cash_capex"] + cal["finance_pay"] + cal["maintenance"] + cal["energy"] + cal["standing"]
    cal["cum_tco"] = cal["total"].cumsum()
    return cal, pd.DataFrame(summaries)


def explain_plan(
    assets_df: pd.DataFrame, spend_df: pd.DataFrame, pay_df: pd.DataFrame,
    min_cash: float, peak_gap: float, car_finance_used: bool,
) -> str:
    """Numbers from *this* run — not a generic blurb."""
    if assets_df.empty or spend_df.empty:
        return "Add inputs in the tabs and this note will describe the plan that was just calculated."
    today = assets_df.iloc[0]
    end = assets_df.iloc[-1]
    cash_low_row = assets_df.loc[assets_df["cash"].idxmin()]
    cash_high_row = assets_df.loc[assets_df["cash"].idxmax()]
    peak = spend_df.loc[spend_df["total"].idxmax()]
    cat_keys = [k for k in ("mortgage", "home", "lifestyle", "family", "cars", "ventures", "investing") if k in spend_df]
    cats = {k: float(spend_df[k].sum()) for k in cat_keys}
    biggest = max(cats, key=cats.get) if cats else "lifestyle"
    peak_cats = {k: float(peak[k]) for k in cat_keys if k in peak}
    peak_lead = max(peak_cats, key=peak_cats.get) if peak_cats else biggest
    labels = {
        "mortgage": "home mortgage repayments", "home": "home running costs and works",
        "lifestyle": "day-to-day lifestyle (incl. medical)", "family": "childcare / college",
        "cars": "cars (deposit, finance and running)", "ventures": "business seed or rental deposit",
        "investing": "monthly investing (saving, not consume)",
    }
    year1_in = float(pay_df["net"].iloc[0]) if pay_df is not None and not pay_df.empty else 0.0
    year1_out = float(spend_df["total"].iloc[0])
    invest_yr = monthly_investments * 12
    lines = []
    lines.append("**This simulation**")
    lines.append(
        f"- Horizon **{comma(time_horizon_years)} years** from {irish_date(planning_start)}, "
        f"retirement age **{comma(retirement_age)}**. Starting cash **{money(plan_start_cash)}** "
        f"({'on' if include_starting_cash else 'off'}). "
        f"Business **{'on' if include_business else 'off'}**, rental **{'on' if include_rental else 'off'}**."
    )
    lines.append(
        f"- **Today’s cash in the bank: {money(today['cash'])}**. "
        f"Liquid investments {money(today['liquid'])}. Illiquid {money(today['illiquid'])}. "
        f"Debts {money(today['liabilities'])}. Net worth {money(today['net_worth'])}."
    )
    lines.append(
        f"- At the horizon: cash {money(end['cash'])}, liquid {money(end['liquid'])}, "
        f"illiquid {money(end['illiquid'])}, debts {money(end['liabilities'])}, "
        f"net worth {money(end['net_worth'])}."
    )
    lines.append("**Cash path in this run**")
    lines.append(
        f"- Lowest bank balance is {money(float(cash_low_row['cash']))} in {int(cash_low_row['year'])}. "
        f"Highest is {money(float(cash_high_row['cash']))} in {int(cash_high_row['year'])}."
    )
    lines.append(
        f"- Year 1 take-home {money(year1_in)} vs cash going out {money(year1_out)} "
        f"(plus {money(invest_yr)} moved into investments)."
    )
    if peak_gap > 1:
        lines.append(
            f"- This run needs extra credit of up to **{money(peak_gap)}**. "
            f"The heaviest spend year is **{int(peak['year'])}** at {money(float(peak['total']))}, "
            f"led by {labels.get(peak_lead, peak_lead)}."
        )
    else:
        lines.append("- The modelled current account stays at or above €0.00 in every year of this run.")
    if pay_df is not None and not pay_df.empty:
        lump_idx = pay_df["net"].idxmax()
        lump_year = int(pay_df.loc[lump_idx, "year"])
        lines.append(
            f"- Highest net-income year is **{lump_year}** at {money(float(pay_df.loc[lump_idx, 'net']))} "
            f"(often the 25% tax-free pension lump). After that, pay is 4% of the remaining pot + State Pension, "
            f"so the green bar **drops** then the pink pot can **climb** if fund growth beats the drawdown."
        )
    lines.append("**Where the money goes in this run**")
    ranked = sorted(cats.items(), key=lambda kv: kv[1], reverse=True)
    for k, v in ranked:
        if v > 0:
            lines.append(f"- {labels.get(k, k)}: **{money(v)}** over the horizon.")
    lines.append(f"- Biggest sink: **{labels.get(biggest, biggest)}**.")
    if not car_finance_used:
        lines.append("- Cars are **cash purchase** in this run (full OTR hits the bank in the buy year).")
    else:
        lines.append("- Cars are on **dealer finance** in this run (deposit + monthly + running).")
    lines.append("**Levers on these exact numbers**")
    lines.append(
        f"- Monthly investing is {money(monthly_investments)} ({money(invest_yr)} / year). "
        "Raise it only if year-1 cash still has slack."
    )
    lines.append(
        f"- Modelled home loan {money(loan)} at {money(pay)} / month. "
        "Overpay is on Housing; it is not an investment sleeve."
    )
    lines.append("*Indicative planner note generated from this run, not advice.*")
    return "\n\n".join(lines)


st.title("Ireland Household Planner")
st.write(
    "Example Irish household calculator for pay, housing, pensions, cars, and investing. "
    "Dates are dd/mm/yyyy. Cash uses 1,234.56. Change the starter numbers to model any household."
)
st.markdown(
    """
    <style>
    button[data-baseweb="tab"] {
        font-size: 1.12rem !important;
        font-weight: 700 !important;
        padding: 0.7rem 1.05rem !important;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.35rem;
        flex-wrap: wrap;
    }
    div[data-testid="stMetric"]:has(div:contains("Cash in the bank")) label,
    [data-testid="stMetric"] {
        background: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
overview = st.container()

snapshot_tab, earners_tab, housing_tab, investments_tab, ventures_tab, auto_tab, family_tab, lifestyle_tab = st.tabs(
    [
        "📸 Snapshot",
        "💼 Earners",
        "🏠 Housing",
        "📈 Investments",
        "🏢 Ventures",
        "🚗 Cars",
        "👨‍👩‍👧 Family",
        "☘️ Lifestyle",
    ]
)
with snapshot_tab:
    st.caption("All of the major charts in one place. Open a named tab to change the inputs behind each graph.")
    snapshot_slot = st.container()

# ---------------------------------------------------------------------------
# Earners — pay, tax, pension, education ROI
# ---------------------------------------------------------------------------
with earners_tab:
    st.subheader("Primary earners")
    st.caption(
        "PAYE model is simplified (single-person bands, standard credits). "
        "It is for planning, not a Revenue computation. Pension relief here is income-tax only; USC still sits on gross."
    )
    n_earners = st.slider("Number of primary earners", 1, 2, 2)
    note("Two PAYE salaries are modelled separately, then added. A side business is on the Ventures tab.")

    earner_rows = []
    household_gross = household_net = household_pension = household_er = 0.0
    earner_cols = st.columns(n_earners, gap="large")
    for i in range(n_earners):
        with earner_cols[i], st.container(border=True):
            st.markdown(f"### Earner {i + 1}")
            g1, g2, g3 = st.columns(3)
            with g1:
                age = st.slider("Age", 22, 67, 30, key=f"earner_age_{i}")
                note("Age sets the max tax-relieved pension % of earnings (15% under 30, up to 40% from 60). Earnings cap ~€115,000.")
            with g2:
                gross = st.number_input(
                    "Gross salary / year (€)", min_value=0.0,
                    value=50_000.0, step=1_000.0, format=MONEY_FMT, key=f"earner_gross_{i}",
                )
                note("Ireland full-time: ~€35k–45k lower; €50k–80k typical professional; €90k+ senior. Dublin often higher.")
            with g3:
                raise_pct = st.slider("Expected raise % / year", 0.0, 12.0, 2.0, 0.1, key=f"earner_raise_{i}")
                note("Cost-of-living 2–3%; promotion years 5–10%.")

            p1, p2, p3 = st.columns(3)
            with p1:
                ee_pct = st.slider("Your pension contribution % of salary", 0.0, 40.0, 5.0, 0.5, key=f"earner_ee_{i}")
                note("Common: 5–7% employee. Higher if catching up. Relief is valuable at 40% income tax. Pension % is on basic salary, not car allowance or BIK.")
            with p2:
                er_pct = st.slider("Employer pension % of salary", 0.0, 20.0, 5.0, 0.5, key=f"earner_er_{i}")
                note("Many Irish employers match 5–7%. Employer money is extra compensation, not from your net pay.")
            with p3:
                start_pension = st.number_input(
                    "Starting pension pot (€)", min_value=0.0,
                    value=0.0, step=1_000.0,
                    format=MONEY_FMT, key=f"earner_pot_{i}",
                )
                note("What is already in this person’s occupational/PRSA/RAC pot today. It then grows with contributions and the assumed return.")

            st.markdown("**Allowances, expenses and extras (separate from salary)**")
            a1, a2 = st.columns(2)
            with a1:
                taxable_allow = st.number_input(
                    "Other taxable allowances / year (€)", min_value=0.0, value=0.0, step=250.0,
                    format=MONEY_FMT, key=f"tax_allow_{i}",
                )
                note("Shift, on-call, location, acting-up: usually PAYE/USC/PRSI like salary.")
            with a2:
                subsistence = st.number_input(
                    "Tax-free subsistence / vouched expenses / year (€)", min_value=0.0, value=0.0, step=100.0,
                    format=MONEY_FMT, key=f"subsist_{i}",
                )
                note("Civil-service-style overnight/day rates or vouched receipts. Not a second salary — keep it to real travel/work costs.")

            car_mode = st.selectbox(
                "Car support (not part of basic salary)",
                [
                    "None",
                    "Taxable cash car allowance",
                    "Tax-free mileage (civil service rates)",
                    "Company car — BIK",
                ],
                key=f"car_mode_{i}",
            )
            car_taxable = car_free = car_bik = 0.0
            if car_mode == "Taxable cash car allowance":
                car_taxable = st.number_input(
                    "Car allowance / year (€)", min_value=0.0, value=5_000.0, step=250.0,
                    format=MONEY_FMT, key=f"car_allow_{i}",
                )
                note("A cash car allowance is almost always taxable. Typical €3,000–8,000; some roles €10,000+.")
            elif car_mode == "Tax-free mileage (civil service rates)":
                car_free = st.number_input(
                    "Mileage reimbursed / year (€)", min_value=0.0, value=2_000.0, step=100.0,
                    format=MONEY_FMT, key=f"car_miles_{i}",
                )
                note("Tax-free only at Revenue/civil-service rates for business km in your own car. Commuting does not count.")
            elif car_mode == "Company car — BIK":
                c1, c2, c3 = st.columns(3)
                with c1:
                    bik_on = st.checkbox("BIK applies", value=True, key=f"car_bik_on_{i}")
                    note("Turn off if the car is pool-use only or otherwise exempt.")
                with c2:
                    omv = st.number_input(
                        "Original market value (€)", min_value=0.0, value=35_000.0, step=1_000.0,
                        format=MONEY_FMT, key=f"car_omv_{i}",
                    )
                with c3:
                    bik_pct = st.slider("BIK % of OMV", 9.0, 37.5, 22.5, 0.5, key=f"car_bik_pct_{i}")
                    note("CO2-based. Petrol/diesel often ~20–30%; many BEVs lower. Indicative, not a Revenue table.")
                car_bik = omv * bik_pct / 100 if bik_on else 0.0

            b1, b2 = st.columns(2)
            with b1:
                bonus = st.number_input(
                    "Christmas / annual bonus (€)", min_value=0.0, value=0.0, step=100.0,
                    format=MONEY_FMT, key=f"bonus_{i}",
                )
                note("A cash bonus through payroll is taxable. A non-cash gift/voucher can use the small-benefit exemption.")
            with b2:
                bonus_free = st.checkbox(
                    "Treat bonus as tax-free small benefit", value=False, key=f"bonus_free_{i}",
                    disabled=bonus <= 0,
                )
                note(f"Small benefit exemption is currently about {money(SMALL_BENEFIT_CAP)} / person / year, and must be a non-cash benefit — not a paid bonus.")
            bonus_taxable = 0.0 if bonus_free else bonus
            bonus_taxfree = min(bonus, SMALL_BENEFIT_CAP) if bonus_free else 0.0
            if bonus_free and bonus > SMALL_BENEFIT_CAP:
                note(f"Amount above {money(SMALL_BENEFIT_CAP)} is treated as taxable cash ({money(bonus - SMALL_BENEFIT_CAP)}).")
                bonus_taxable = bonus - SMALL_BENEFIT_CAP

            other_bik_on = st.checkbox("Other BIK applies (health cover, van, preferential loan, etc.)", value=False, key=f"other_bik_on_{i}")
            other_bik = 0.0
            if other_bik_on:
                other_bik = st.number_input(
                    "Other BIK / year (€)", min_value=0.0, value=1_200.0, step=50.0,
                    format=MONEY_FMT, key=f"other_bik_{i}",
                )
                note("Employer-paid medical insurance is a common BIK. Tick only if Revenue would treat it as a benefit.")

            cash_taxable = gross + taxable_allow + car_taxable + bonus_taxable
            tax_free_cash = subsistence + car_free + bonus_taxfree
            bik_total = car_bik + other_bik

            cap = 115_000.0
            max_pct = pension_age_limit_pct(age)
            ee_amt = min(gross * ee_pct / 100, cap * max_pct)
            er_amt = gross * er_pct / 100
            pack = irish_paye(cash_taxable, ee_amt, bik=bik_total, tax_free_cash=tax_free_cash)
            clipped = gross * ee_pct / 100 > ee_amt + 1
            if clipped:
                note(f"Employee contribution clipped to the age-related max ({max_pct:.0%} of earnings, cap {money(cap)}).")

            t1, t2 = st.columns(2)
            t1.metric("Income tax / year", money(pack["income_tax"]))
            t2.metric("USC + PRSI / year", money(pack["usc"] + pack["prsi"]))
            t3, t4 = st.columns(2)
            t3.metric("BIK (not cash)", money(bik_total))
            t4.metric("Tax-free cash", money(tax_free_cash))
            st.metric("Net take-home / year", money(pack["net"]), delta=money(pack["net"] / 12) + " / month")
            st.caption(
                f"Effective tax on emoluments ~{pack['effective']:.0%}. "
                f"Pension this year: you {money(ee_amt)} + employer {money(er_amt)} = {money(ee_amt + er_amt)} into the pot "
                f"(starting pot {money(start_pension)})."
            )

            st.markdown("**Education / career investment for this earner**")
            e1, e2, e3 = st.columns(3)
            with e1:
                edu_cost = st.number_input(
                    "Upfront cost from net pay (€)", min_value=0.0, value=0.0,
                    step=500.0, key=f"edu_cost_{i}",
                )
                note("Part-time MSc/certs €3k–12k; MBA €20k–50k. Paid from after-tax cash unless employer-funded.")
            with e2:
                edu_uplift = st.number_input(
                    "Extra gross salary from it (€ / year)", min_value=0.0, value=0.0,
                    step=500.0, key=f"edu_uplift_{i}",
                )
                note("Be conservative: not every course moves pay. €3k–10k is a solid professional bump.")
            with e3:
                edu_years = st.slider("Years the extra pay lasts", 1, 25, 10, key=f"edu_years_{i}")

            extra_net = 0.0
            payback = None
            if edu_uplift > 0:
                after = irish_paye(
                    cash_taxable + edu_uplift,
                    min((gross + edu_uplift) * ee_pct / 100, cap * max_pct),
                    bik=bik_total, tax_free_cash=tax_free_cash,
                )
                extra_net = after["net"] - pack["net"]
                payback = edu_cost / extra_net if extra_net > 0 else None
                lifetime_gain = extra_net * edu_years - edu_cost
                r1, r2, r3 = st.columns(3)
                r1.metric("Extra net pay / year", money(extra_net))
                r2.metric("Simple payback", f"{payback:,.1f} years" if payback else "—")
                r3.metric(f"Net gain over {comma(edu_years)}y", money(lifetime_gain))
                note(
                    "ROI uses today’s tax bands on the extra slice of salary (often ~48–52% gone at the higher rate). "
                    "If the employer pays the course, treat cost as €0 here."
                )

            household_gross += cash_taxable
            household_net += pack["net"]
            household_pension += ee_amt
            household_er += er_amt
            earner_rows.append(
                {
                    "age": age, "gross": gross, "raise": raise_pct, "ee": ee_amt, "er": er_amt,
                    "net": pack["net"], "pack": pack, "edu_cost": edu_cost, "edu_uplift": extra_net,
                    "taxable_extras": cash_taxable - gross, "tax_free": tax_free_cash, "bik": bik_total,
                    "start_pension": start_pension,
                }
            )

    st.markdown("**Household cash this year**")
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Combined taxable pay", money(household_gross))
    h2.metric("Combined net take-home", money(household_net), delta=money(household_net / 12) + " / month")
    h3.metric("Your pension contributions", money(household_pension))
    h4.metric("Employer pension (extra)", money(household_er))
    note(
        f"Sidebar ‘monthly investments’ is still {money(monthly_investments)} / month. "
        "Use take-home minus mortgage, lifestyle and childcare to see what is actually investable."
    )

    years = list(range(planning_start.year, planning_start.year + time_horizon_years + 1))
    pay_rows = []
    pots = [float(erow.get("start_pension", 0.0)) for erow in earner_rows]
    r_pen = (1 + annual_return / 100)
    retired_flags = [False] * n_earners
    for yi, yr in enumerate(years):
        year_net = year_gross = year_pen = year_draw = 0.0
        for i, erow in enumerate(earner_rows):
            age_now = erow["age"] + yi
            if age_now < retirement_age:
                g = erow["gross"] * (1 + erow["raise"] / 100) ** yi
                ee = g * (earner_rows[i]["ee"] / erow["gross"] if erow["gross"] else 0)
                er = g * (earner_rows[i]["er"] / erow["gross"] if erow["gross"] else 0)
                pack = irish_paye(
                    g + erow.get("taxable_extras", 0.0), ee,
                    bik=erow.get("bik", 0.0), tax_free_cash=erow.get("tax_free", 0.0),
                )
                pots[i] = pots[i] * r_pen + ee + er
                year_gross += g + erow.get("taxable_extras", 0.0)
                year_net += pack["net"]
            else:
                pots[i] *= r_pen
                if not retired_flags[i]:
                    lump = pots[i] * 0.25
                    pots[i] -= lump
                    year_net += lump
                    year_draw += lump
                    retired_flags[i] = True
                rate = 0.04 if age_now < 71 else 0.05
                draw = pots[i] * rate
                pots[i] = max(pots[i] - draw, 0.0)
                pack = irish_paye(draw + STATE_PENSION, 0.0)
                year_gross += draw + STATE_PENSION
                year_net += pack["net"]
                year_draw += draw
            year_pen += pots[i]
        pay_rows.append(
            {"year": yr, "gross": year_gross, "net": year_net, "pension_pots": year_pen, "drawdown": year_draw}
        )
    pay_df = pd.DataFrame(pay_rows)
    retire_year = planning_start.year + max(retirement_age - earner_rows[0]["age"], 0) if earner_rows else None
    pay_fig = go.Figure()
    pay_fig.add_trace(go.Bar(name="Gross (salary / then pension income)", x=pay_df["year"], y=pay_df["gross"].map(to_display), marker_color="#4C78A8"))
    pay_fig.add_trace(go.Bar(name="Net cash (pay or drawdown)", x=pay_df["year"], y=pay_df["net"].map(to_display), marker_color="#54A24B"))
    pay_fig.add_trace(go.Scatter(
        name="Pension pots (in fund)", x=pay_df["year"],
        y=pay_df["pension_pots"].map(to_display), mode="lines+markers", line=dict(width=3), yaxis="y2",
    ))
    add_plan_markers(pay_fig, planning_start.year, retire_year, plan_start_cash)
    pay_fig.update_layout(
        barmode="group", title="Pay while working, then pension drawdown after retirement",
        xaxis_title="Calendar year", yaxis_title=currency_label,
        yaxis=dict(tickformat=",.2f", tickprefix=cur, exponentformat="none"),
        yaxis2=dict(
            title="Pension pots", overlaying="y", side="right",
            tickformat=",.2f", tickprefix=cur, exponentformat="none", separatethousands=True,
        ),
        hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=60, r=70, t=70, b=20),
    )
    pay_left, pay_right = st.columns([1.7, 1], vertical_alignment="top")
    with pay_left:
        plot_money(pay_fig, snap="Pay and pension pots")
    with pay_right:
        lump_year = int(pay_df.loc[pay_df["net"].idxmax(), "year"]) if not pay_df.empty else planning_start.year
        advice_box(
            "Why pay dips, then the pot climbs",
            [
                f"Until age {comma(retirement_age)} the bars are salary (raises continue).",
                f"The **first retired year** (often {lump_year}) adds a **25% tax-free lump** from the pension pot — that is the spike in net cash, and the pink line **drops** by that lump.",
                "After that you take **4% of what is left** each year (5% from 71) plus an indicative State Pension of "
                f"{money(STATE_PENSION)}. That is usually **less than salary**, so the green/blue bars fall.",
                "The pink pot can **rise again** if the assumed fund return is higher than the 4–5% you draw. It is still illiquid until you draw it.",
                "Drawdown is taxed as income. This is a planning rule of thumb, not an ARF quote.",
            ],
        )

# ---------------------------------------------------------------------------
# Housing
# ---------------------------------------------------------------------------
with housing_tab:
    st.subheader("Housing & mortgage")
    h1, h2, h3, h4 = st.columns(4)
    with h1:
        housing_country = st.selectbox("Mortgage market", list(MORTGAGE_MARKETS.keys()), index=0)
    with h2:
        deposit_pct = st.radio("Deposit tier", [10, 20, 30], index=1, horizontal=True, format_func=lambda x: f"{x}%")
    with h3:
        mortgage_term = st.slider("Term (years)", 10, 35, 30, 1)
    with h4:
        house_date = date_field("Target purchase date", date(planning_start.year + 1, 1, 1), key="house_date")

    hp1, hp2, hp3 = st.columns(3)
    with hp1:
        purchase_price = st.number_input(
            "House purchase price (€)", min_value=0.0, value=float(home_value), step=5_000.0,
            format=MONEY_FMT, key="house_purchase",
        )
        note("This can differ from the sidebar ‘home value’ if you already own and are modelling a new loan, or vice versa.")
    with hp2:
        loan = st.number_input(
            "Mortgage amount (€)", min_value=0.0,
            value=float(home_value) * 0.80, step=5_000.0, format=MONEY_FMT, key="house_loan",
        )
        note("Type the loan you will actually draw. Deposit is price minus this amount.")
    with hp3:
        extra_overpay = st.number_input("Optional extra monthly repayment (€)", min_value=0.0, value=0.0, step=50.0)
        note("On top of the scheduled monthly. €0 = timetable only. €100–250/month is a common extra.")
    mkt = MORTGAGE_MARKETS[housing_country]
    quoted_rate = mkt["rates"][deposit_pct]
    rate_used = st.slider(
        "Interest rate (annual %)", 1.0, 8.0, float(quoted_rate), 0.05,
        help=f"Default is the {housing_country} {deposit_pct}% deposit bracket ({quoted_rate:.2f}%).",
    )
    st.caption(mkt["note"] + f" Drawdown modelled from {irish_date(house_date)}.")

    if housing_country == "Ireland":
        st.markdown("**Indicative Irish lender rates for this deposit and term**")
        term_key = 30 if mortgage_term >= 28 else (20 if mortgage_term >= 18 else 20)
        bank_rows = []
        for b in IRISH_BANKS:
            rate_b = irish_bank_rate(b["bank"], deposit_pct, mortgage_term)
            bank_rows.append(
                {
                    "Lender": b["bank"],
                    "Indicative rate": f"{rate_b:.2f}%",
                    "Monthly on this loan": money(standard_payment(loan, rate_b, mortgage_term)),
                }
            )
        st.dataframe(pd.DataFrame(bank_rows), hide_index=True, width="stretch")
        note(
            "Owner-occupier **fixed** talking ranges, not a quote. 10% deposit is high-LTV (dearest); "
            f"20% is the volume band; 30% is high-equity. Your slider is at **{rate_used:.2f}%** for a **{mortgage_term}-year** term. "
            "AIB / BOI / PTSB / EBS / Haven often sit within ~0.3pp of each other on the same LTV."
        )

    deposit_amt = max(purchase_price - loan, 0.0)
    stamp = purchase_price * mkt["stamp"]
    cash_to_buy = deposit_amt + stamp
    sched = amortize(loan, rate_used, mortgage_term, 0.0)
    over = amortize(loan, rate_used, mortgage_term, extra_overpay)
    pay = standard_payment(loan, rate_used, mortgage_term)
    st.markdown(
        f"<div style='background:#1f3d2a;border:2px solid #54A24B;border-radius:12px;padding:14px 18px;margin:8px 0 16px 0;'>"
        f"<div style='color:#a8e6bf;font-size:0.85rem;'>MONTHLY REPAYMENT AT {rate_used:.2f}% OVER {mortgage_term} YEARS</div>"
        f"<div style='color:#ffffff;font-size:2.1rem;font-weight:700;'>{money(pay)}</div>"
        f"<div style='color:#cfe8d8;'>Loan {money(loan)} · {money(pay * 12)} / year"
        f"{' · plus extra ' + money(extra_overpay) + ' / month' if extra_overpay else ''}</div></div>",
        unsafe_allow_html=True,
    )
    base_interest = float(sched["cum_interest"].iloc[-1]) if not sched.empty else 0.0
    over_interest = float(over["cum_interest"].iloc[-1]) if not over.empty else 0.0
    years_saved = float(sched["year"].iloc[-1] - over["year"].iloc[-1]) if not sched.empty and not over.empty else 0.0
    if not sched.empty:
        sched = sched.copy()
        sched["calendar_year"] = house_date.year + sched["year"] - 1
    if not over.empty:
        over = over.copy()
        over["calendar_year"] = house_date.year + over["year"] - 1

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Mortgage amount (loan)", money(loan))
    k2.metric("Monthly repayment", money(pay), delta=money(pay * 12) + " / year")
    k3.metric(
        "Deposit (price − loan)",
        money(deposit_amt),
        delta=(f"{deposit_amt / purchase_price:.0%} of price" if purchase_price else "—"),
    )
    k4.metric("Rate used", f"{rate_used:.2f}%")
    k5.metric("Cash to complete (deposit + duty)", money(cash_to_buy))

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total interest if you never overpay", money(base_interest))
    s2.metric("Interest as % of house price", f"{base_interest / purchase_price:.0%}" if purchase_price else "—")
    s3.metric("Interest vs the deposit", f"{base_interest / deposit_amt:.1f}×" if deposit_amt else "—")
    s4.metric(
        "Interest saved if you overpay",
        money(base_interest - over_interest) if extra_overpay else money(0),
        delta=(f"{years_saved:.1f}y shorter" if extra_overpay else "no extra set"),
    )
    st.caption(
        f"You send the lender {money(pay)} every month ({money(pay * 12)} / year). Over the full term that is "
        f"{money(loan + base_interest)}: {money(loan)} of loan plus {money(base_interest)} of interest. "
        "The leftover mortgage balance is a debt, not cash leaving the bank that day."
    )

    stacked = go.Figure()
    stacked.add_trace(go.Bar(
        name="Total paid that year (below axis)",
        x=sched["calendar_year"],
        y=(-(sched["principal"] + sched["interest"])).map(to_display),
        marker_color="rgba(160,160,160,0.45)",
    ))
    stacked.add_trace(go.Bar(name="Principal repaid", x=sched["calendar_year"], y=sched["principal"].map(to_display), marker_color="#4C78A8"))
    stacked.add_trace(go.Bar(name="Interest paid", x=sched["calendar_year"], y=sched["interest"].map(to_display), marker_color="#E45756"))
    stacked.add_trace(go.Scatter(
        name="Cumulative paid to lender",
        x=sched["calendar_year"],
        y=(sched["cum_interest"] + loan - sched["balance"]).map(to_display),
        mode="lines", line=dict(width=3, color="#9D755D"), yaxis="y2",
    ))
    stacked.update_layout(
        barmode="relative", title="Each year: interest vs principal (grey = total paid, below the axis)",
        xaxis_title="Calendar year", yaxis_title=currency_label, yaxis_tickformat=tick,
        yaxis2=dict(title="Cumulative paid", overlaying="y", side="right", tickformat=tick),
        hovermode="x unified",
    )
    donut = go.Figure(go.Pie(
        labels=["Principal (the house loan)", "Interest (cost of borrowing)"],
        values=[to_display(loan), to_display(base_interest)],
        hole=0.55, marker_colors=["#4C78A8", "#E45756"], textinfo="label+percent",
    ))
    donut.update_layout(title="Total money sent to the lender", showlegend=False)
    curves = go.Figure()
    if not sched.empty:
        curves.add_trace(go.Scatter(
            x=sched["calendar_year"], y=sched["balance"].map(to_display),
            name="Debt still owed", line=dict(width=3, color="#E45756"),
        ))
        curves.add_trace(go.Scatter(
            x=sched["calendar_year"], y=sched["cum_interest"].map(to_display),
            name="Interest paid so far", line=dict(width=3, color="#F58518"),
        ))
        curves.add_trace(go.Scatter(
            x=sched["calendar_year"],
            y=(purchase_price - sched["balance"]).map(to_display),
            name="Home equity (value − debt)", line=dict(width=3, color="#54A24B"),
        ))
        curves.update_layout(
            title="Equity vs interest vs remaining debt",
            xaxis_title="Calendar year", yaxis_title=currency_label, hovermode="x unified", height=380,
        )

    mort_advice = [
        f"Loan **{money(loan)}**, **{money(pay)} / month**, rate **{rate_used:.2f}%**, term **{mortgage_term} years**.",
        f"Never-overpay interest is **{money(base_interest)}** — that is {base_interest / purchase_price:.0%} of the house price." if purchase_price else "Set a house value in the sidebar.",
        "Grey bars below zero are the **same year’s total cash to the lender** (interest + principal), so you can see the full payment against the split above the axis.",
        f"Extra overpay is **{money(extra_overpay)} / month**. "
        + (f"That saves about {money(base_interest - over_interest)} interest and {years_saved:.1f} years." if extra_overpay else "Try €100–250 to see the interest line flatten."),
        "A cheaper band is usually a **bigger deposit** (20% vs 10%) or a slightly shorter fix — use the bank table, then move the rate slider.",
        "Overpaying is not investing: it only cuts interest and the term. Compare that saving with the Investments tab return after tax.",
    ]
    mode = str(st.session_state.get("chart_place", "Beside inputs"))
    if mode.startswith("Beside"):
        c_in, c_ch = st.columns([1, 1.4], vertical_alignment="top")
        with c_in:
            advice_box("Mortgage — what this run is doing", mort_advice)
        with c_ch:
            plot_money(stacked, snap="Mortgage interest vs principal")
            plot_money(donut)
            if not sched.empty:
                plot_money(curves, snap="Equity vs interest vs debt")
    else:
        plot_money(stacked, snap="Mortgage interest vs principal")
        d1, d2 = st.columns(2)
        with d1:
            plot_money(donut)
        with d2:
            advice_box("Mortgage — what this run is doing", mort_advice)
        if not sched.empty:
            plot_money(curves, snap="Equity vs interest vs debt")

    st.markdown("**Home running costs, maintenance and works**")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        home_ins = st.number_input("Buildings + contents insurance / year (€)", min_value=0.0, value=800.0, step=50.0)
        note("Typical Ireland: €500–700 modest house; €800–1,200 average; €1,500+ higher rebuild / Dublin contents.")
    with r2:
        maint_pct = st.slider("Maintenance allowance (% of home value / year)", 0.0, 3.0, 1.0, 0.1)
        st.caption(f"= **{money(home_value * maint_pct / 100)} / year** on a {money(home_value)} home.")
        note("Rule of thumb: 0.5% light; 1% standard sinking fund; 1.5–2% older houses.")
    with r3:
        n_works = st.slider("Renovation / extension projects", 0, 3, 0)
        note("Kitchen €15k–40k; single-storey extension €40k–90k; larger/two-storey €90k–180k+ (indicative).")
    with r4:
        lpt = st.number_input("Local property tax / year (€)", min_value=0.0, value=400.0, step=25.0, format=MONEY_FMT)
        note("LPT is banded on value. Many 3-bed houses sit roughly €300–700.")

    u1, u2, u3 = st.columns(3)
    with u1:
        power_y = st.number_input("Electricity / year (€)", min_value=0.0, value=1_500.0, step=50.0, format=MONEY_FMT)
        note("Typical Irish house: ~€1,200–2,200 depending on heat source and BER.")
    with u2:
        heat_y = st.number_input("Heat (gas / oil / heat pump extra) / year (€)", min_value=0.0, value=1_200.0, step=50.0, format=MONEY_FMT)
        note("Gas 3-bed often €1,000–1,800; oil higher; heat-pump kWh often sits in the electricity line instead.")
    with u3:
        bb_y = st.number_input("Broadband / year (€)", min_value=0.0, value=600.0, step=24.0, format=MONEY_FMT)
        note("Fibre ~€40–60 / month (€480–720 / year).")

    works: list[dict] = []
    for i in range(n_works):
        with st.expander(f"Works {i + 1}", expanded=(i == 0)):
            w1, w2, w3 = st.columns(3)
            with w1:
                w_date = date_field("Target date", date(house_date.year + 2 + i * 3, 4, 1), key=f"works_date_{i}")
            with w2:
                w_cost = st.number_input("Budget (€)", min_value=0.0, value=20_000.0, step=1_000.0, key=f"works_cost_{i}")
            with w3:
                w_uplift = st.slider("Estimated value added (%)", 0, 80, 40, key=f"works_uplift_{i}")
                st.caption(
                    f"Spend {money(w_cost)} → estimated extra house value **{money(w_cost * w_uplift / 100)}** "
                    f"({w_uplift:.0f}%). The other {money(w_cost * (1 - w_uplift / 100))} is lifestyle/comfort, not equity."
                )
            works.append({"date": w_date, "cost": w_cost, "uplift": w_uplift / 100})

    maint_annual = home_value * maint_pct / 100
    home_years = list(range(house_date.year, planning_start.year + time_horizon_years + 1))
    home_rows = []
    added_value = 0.0
    cum_run = 0.0
    for yr in home_years:
        ins = home_ins
        maint = maint_annual
        utils = power_y + heat_y + bb_y + lpt
        reno = sum(w["cost"] for w in works if w["date"].year == yr)
        added_value += sum(w["cost"] * w["uplift"] for w in works if w["date"].year == yr)
        total = ins + maint + reno + utils
        cum_run += total
        home_rows.append({
            "year": yr, "insurance": ins, "maintenance": maint, "works": reno,
            "utilities": utils, "total": total, "cumulative": cum_run,
        })
    home_run = pd.DataFrame(home_rows)
    hr1, hr2, hr3 = st.columns(3)
    hr1.metric("Annual insurance", money(home_ins))
    hr2.metric("Annual maintenance allowance", money(maint_annual))
    hr3.metric("Works budget in horizon", money(sum(w["cost"] for w in works)), delta=f"value add {money(added_value)}")

    if not home_run.empty:
        home_fig = go.Figure()
        home_fig.add_trace(go.Bar(name="Insurance", x=home_run["year"], y=home_run["insurance"].map(to_display), marker_color="#4C78A8"))
        home_fig.add_trace(go.Bar(name="Maintenance", x=home_run["year"], y=home_run["maintenance"].map(to_display), marker_color="#F58518"))
        home_fig.add_trace(go.Bar(name="Power / heat / broadband / LPT", x=home_run["year"], y=home_run["utilities"].map(to_display), marker_color="#B279A2"))
        home_fig.add_trace(go.Bar(name="Renovations / extensions", x=home_run["year"], y=home_run["works"].map(to_display), marker_color="#E45756"))
        home_fig.add_trace(go.Scatter(
            name="Lifetime spend (cumulative)", x=home_run["year"], y=home_run["cumulative"].map(to_display),
            mode="lines", line=dict(width=3, color="#9D755D"), yaxis="y2",
        ))
        home_fig.update_layout(
            barmode="stack", title="Home running costs and works by year",
            xaxis_title="Calendar year", yaxis_title=currency_label, yaxis_tickformat=tick,
            yaxis2=dict(title="Lifetime spend", overlaying="y", side="right", tickformat=tick),
            hovermode="x unified",
        )
        h_in, h_ch = st.columns([1, 1.4], vertical_alignment="top") if str(st.session_state.get("chart_place", "Beside")).startswith("Beside") else (None, None)
        home_advice = [
            f"Year-1 running cost **{money(float(home_run['total'].iloc[0]))}** including utilities.",
            f"Lifetime spend on this chart: **{money(float(home_run['cumulative'].iloc[-1]))}**.",
            "Energy upgrades (below) cut the electricity/heat lines; the brown line is cumulative cash out.",
            "A 1% maintenance sinking fund is boring and is what stops a €20k boiler year from emptying the bank.",
        ]
        if h_ch is not None:
            with h_in:
                advice_box("Home costs — this run", home_advice)
            with h_ch:
                plot_money(home_fig, snap="Home running costs")
        else:
            plot_money(home_fig, snap="Home running costs")
            advice_box("Home costs — this run", home_advice)

    st.markdown("**Renewables: solar, heat pump and grants**")
    st.caption("Indicative Irish installed costs and SEAI-style grants. Toggle “apply for grant” per measure; amounts are editable.")
    measures = [
        {"id": "pv", "label": "Solar PV", "cost": 9_500, "grant": 1_800, "save": 950, "life": 25},
        {"id": "bat", "label": "Home battery", "cost": 6_500, "grant": 0, "save": 220, "life": 12},
        {"id": "ashp", "label": "Air-to-water heat pump", "cost": 16_500, "grant": 6_500, "save": 1_100, "life": 18},
        {"id": "st", "label": "Solar thermal (hot water)", "cost": 4_200, "grant": 1_200, "save": 180, "life": 20},
        {"id": "insul", "label": "Attic + wall insulation", "cost": 8_000, "grant": 4_000, "save": 350, "life": 30},
    ]
    reno_rows = []
    for mitem in measures:
        with st.expander(mitem["label"], expanded=False):
            on = st.checkbox("Include this measure", value=False, key=f"rn_on_{mitem['id']}")
            g1, g2, g3, g4 = st.columns(4)
            with g1:
                cost = st.number_input("Installed cost (€)", min_value=0.0, value=float(mitem["cost"]), step=250.0, key=f"rn_cost_{mitem['id']}")
            with g2:
                apply_grant = st.checkbox("Apply for grant", value=True, key=f"rn_grant_on_{mitem['id']}")
            with g3:
                grant = st.number_input("Grant if approved (€)", min_value=0.0, value=float(mitem["grant"]), step=100.0, key=f"rn_grant_{mitem['id']}")
            with g4:
                save = st.number_input("Est. annual saving (€)", min_value=0.0, value=float(mitem["save"]), step=25.0, key=f"rn_save_{mitem['id']}")
            install = date_field("Install date", date(house_date.year, 9, 1), key=f"rn_date_{mitem['id']}")
            net_cost = max(cost - (grant if apply_grant else 0.0), 0.0)
            payback = net_cost / save if save else None
            if on:
                reno_rows.append(
                    {
                        "Measure": mitem["label"], "Install": irish_date(install), "year": install.year,
                        "Gross cost": cost, "Grant": grant if apply_grant else 0.0, "Net cost": net_cost,
                        "Annual saving": save, "Simple payback (y)": payback if payback is not None else 0.0,
                    }
                )
    if reno_rows:
        rdf = pd.DataFrame(reno_rows)
        st.dataframe(
            rdf.assign(**{
                "Gross cost": rdf["Gross cost"].map(money),
                "Grant": rdf["Grant"].map(money),
                "Net cost": rdf["Net cost"].map(money),
                "Annual saving": rdf["Annual saving"].map(money),
                "Simple payback (y)": rdf["Simple payback (y)"].map(lambda x: f"{x:,.1f}" if x else "—"),
            }),
            hide_index=True, width="stretch",
        )
        rr1, rr2, rr3 = st.columns(3)
        rr1.metric("Net capital (after grants)", money(sum(r["Net cost"] for r in reno_rows)))
        rr2.metric("Grants assumed approved", money(sum(r["Grant"] for r in reno_rows)))
        rr3.metric("Combined annual saving", money(sum(r["Annual saving"] for r in reno_rows)))
        save_fig = go.Figure()
        years_axis = list(range(0, 26))
        annual_s = sum(r["Annual saving"] for r in reno_rows)
        net_c = sum(r["Net cost"] for r in reno_rows)
        save_fig.add_trace(go.Scatter(
            name="Cumulative energy saving", x=years_axis,
            y=[to_display(annual_s * y) for y in years_axis],
            line=dict(width=3, color="#54A24B"),
        ))
        save_fig.add_hline(
            y=to_display(net_c), line_dash="dash", line_color="#E45756",
            annotation_text=f"Net capital {money(net_c)}",
        )
        save_fig.update_layout(
            title="Energy upgrades: payback (saving vs net capital)",
            xaxis_title="Years after install", yaxis_title=currency_label, hovermode="x unified",
        )
        plot_money(save_fig, snap="Energy upgrade payback")
        note(
            f"Simple payback ~ **{(net_c / annual_s):.1f} years** if savings stay flat. "
            "Grants are assumed approved. Real bills also move with unit rates and how you heat the house."
            if annual_s else "Set an annual saving to see payback."
        )

    st.dataframe(
        over.assign(**{
            "Year": over["calendar_year"].map(comma),
            "Interest that year": over["interest"].map(money),
            "Principal that year": over["principal"].map(money),
            "Balance": over["balance"].map(money),
            "Interest (cum.)": over["cum_interest"].map(money),
        })[["Year", "Interest that year", "Principal that year", "Balance", "Interest (cum.)"]],
        hide_index=True, width="stretch", height=240,
    )

# ---------------------------------------------------------------------------
# Investments
# ---------------------------------------------------------------------------
with investments_tab:
    st.subheader("Investments — sleeves and Irish tax")
    i0, i1, i2, i3 = st.columns(4)
    with i0:
        st.number_input(
            "Current investment pot (€)",
            min_value=0.0, step=1_000.0, format="%.2f", key="existing_investments",
            help="What you already hold in ETFs/shares today. This is liquid investments, not cash in the bank.",
        )
        note("Put today’s portfolio here. Starting cash on the master graph is the current account only.")
    with i1:
        st.metric("Monthly contribution", money(monthly_investments), delta="from sidebar")
    with i2:
        st.metric("Annual contribution", money(monthly_investments * 12))
    with i3:
        st.metric("Existing pot in this run", money(float(st.session_state.existing_investments)))
    existing_investments = float(st.session_state.existing_investments)
    st.markdown(
        """
What each sleeve *means* (indicative Irish tax, not advice):

| Sleeve | What it is | Tax while you hold | Tax when you sell / every 8 years |
| --- | --- | --- | --- |
| **UCITS ETF** | Broad funds (world/S&P) | None inside the fund | **41% exit tax** and **deemed disposal every 8 years** |
| **Dividend Kings** | High-quality dividend shares | **33%** on dividends | **33% CGT** on gains |
| **Common stocks** | Ordinary growth shares | **33%** on any small dividend | **33% CGT** on gains |
| **ROCE / quality** | Compounders with high return on capital | **33%** on modest dividends | **33% CGT** on gains |
| **Bonds (UCITS)** | Gov/aggregate bond funds | None inside the fund | **41% exit tax** and **8-year deemed disposal** |

Pensions (Earners tab) are separate: growth is tax-free in the fund.
        """
    )

    st.markdown("**Split of taxable investing (existing pot + monthly contribution)**")
    note("Weights are scaled to 100% if they do not add up. This is the taxable pot, not the pension.")
    a1, a2, a3, a4, a5 = st.columns(5)
    with a1:
        w_etf = st.slider("UCITS ETF %", 0, 100, 30, 5)
        note("Simple, diversified — but 41% and 8-year deemed disposal is a real drag vs shares.")
    with a2:
        w_bonds = st.slider("Bonds %", 0, 100, 15, 5)
        note("Bond UCITS in Ireland is usually the same 41% exit tax as equity ETFs.")
    with a3:
        w_kings = st.slider("Dividend Kings %", 0, 100, 15, 5)
        note("Cash yield each year, taxed 33%, even if you reinvest.")
    with a4:
        w_common = st.slider("Common stocks %", 0, 100, 20, 5)
        note("More price growth, little dividend. CGT only when you (or we, at the horizon) sell.")
    with a5:
        w_roce = st.slider("ROCE / quality %", 0, 100, 20, 5)
        note("Quality compounders: assume slightly higher growth, still 33%/33% share tax.")

    wsum = w_etf + w_bonds + w_kings + w_common + w_roce
    if wsum <= 0:
        weights = {"etf": 1.0, "bonds": 0.0, "kings": 0.0, "common": 0.0, "roce": 0.0}
    else:
        weights = {
            "etf": w_etf / wsum, "bonds": w_bonds / wsum, "kings": w_kings / wsum,
            "common": w_common / wsum, "roce": w_roce / wsum,
        }
    st.caption(
        f"Using ETF {weights['etf']:.0%} · Bonds {weights['bonds']:.0%} · Kings {weights['kings']:.0%} · "
        f"Common {weights['common']:.0%} · ROCE {weights['roce']:.0%}."
    )

    s1, s2, s3, s4, s5 = st.columns(5)
    with s1:
        etf_return = st.slider("ETF gross return %", 0.0, 12.0, float(annual_return), 0.1)
    with s2:
        bond_return = st.slider("Bond gross return %", 0.0, 8.0, 3.2, 0.1)
        note("Indicative euro aggregate / Irish gov mix. Not a yield quote.")
    with s3:
        king_growth = st.slider("Kings price growth %", 0.0, 12.0, 6.0, 0.1)
        king_yield = st.slider("Kings dividend yield %", 0.0, 6.0, 2.8, 0.1)
    with s4:
        common_growth = st.slider("Common stocks growth %", 0.0, 14.0, 8.0, 0.1)
        common_yield = st.slider("Common stocks yield %", 0.0, 3.0, 0.6, 0.1)
    with s5:
        roce_growth = st.slider("ROCE growth %", 0.0, 14.0, 9.0, 0.1)
        roce_yield = st.slider("ROCE yield %", 0.0, 4.0, 1.2, 0.1)

    note(
        "This tab is the investment sleeves only. Putting extra cash on the **mortgage** (an overpayment) is on the Housing tab. "
        "An overpayment is not an investment: it only reduces interest and the loan term."
    )

    def sleeve(weight: float, fn, *args):
        return fn(existing_investments * weight, monthly_investments * weight, time_horizon_years, *args)

    etf = sleeve(weights["etf"], project_ucits_etf, etf_return)
    bonds = sleeve(weights["bonds"], project_ucits_etf, bond_return)
    kings = sleeve(weights["kings"], project_equity_sleeve, king_growth, king_yield)
    common = sleeve(weights["common"], project_equity_sleeve, common_growth, common_yield)
    roce = sleeve(weights["roce"], project_equity_sleeve, roce_growth, roce_yield)

    def last_net(df: pd.DataFrame) -> float:
        return float(df["net_value"].iloc[-1]) if not df.empty else 0.0

    def last_tax(df: pd.DataFrame) -> float:
        return float(df["tax_paid"].iloc[-1]) if not df.empty else 0.0

    mix_end = last_net(etf) + last_net(bonds) + last_net(kings) + last_net(common) + last_net(roce)
    mix_tax = last_tax(etf) + last_tax(bonds) + last_tax(kings) + last_tax(common) + last_tax(roce)

    st.markdown(
        f"<div style='background:#1a2a3a;border:2px solid #4C78A8;border-radius:12px;padding:12px 16px;margin:6px 0 12px 0;'>"
        f"<div style='color:#a8c6e6;font-size:0.85rem;'>COMBINED INVESTMENT VALUE (AFTER TAX)</div>"
        f"<div style='color:#ffffff;font-size:2rem;font-weight:700;'>{money(mix_end)}</div>"
        f"<div style='color:#c5d8ea;'>Tax paid/reserved {money(mix_tax)} · existing pot {money(existing_investments)} · "
        f"{money(monthly_investments)} / month in</div></div>",
        unsafe_allow_html=True,
    )
    n1, n2, n3, n4, n5 = st.columns(5)
    n1.metric("ETF sleeve (after 41%)", money(last_net(etf)))
    n2.metric("Bonds (after 41%)", money(last_net(bonds)))
    n3.metric("Kings sleeve (after 33%)", money(last_net(kings)))
    n4.metric("Common stocks (after 33%)", money(last_net(common)))
    n5.metric("ROCE sleeve (after 33%)", money(last_net(roce)))

    years_i = next((df["year"] for df in (etf, bonds, kings, common, roce) if not df.empty), pd.Series(dtype=float))
    contrib_line, tax_line, net_line = [], [], []
    xs = []
    if not years_i.empty:
        for yr in years_i:
            xs.append(yr)
            n = t = c = 0.0
            for df, wkey in ((etf, "etf"), (bonds, "bonds"), (kings, "kings"), (common, "common"), (roce, "roce")):
                if weights[wkey] <= 0 or df.empty:
                    continue
                row = df.loc[(df["year"] - yr).abs().idxmin()]
                n += float(row["net_value"])
                t += float(row["tax_paid"])
                c += float(row.get("contributed", 0.0))
            net_line.append(n)
            tax_line.append(t)
            contrib_line.append(c)

    inv_fig = go.Figure()
    if weights["etf"] > 0 and not etf.empty:
        inv_fig.add_trace(go.Scatter(x=etf["year"], y=etf["net_value"].map(to_display), name="UCITS ETF (after tax)", line=dict(width=3)))
    if weights["bonds"] > 0 and not bonds.empty:
        inv_fig.add_trace(go.Scatter(x=bonds["year"], y=bonds["net_value"].map(to_display), name="Bonds (after 41%)", line=dict(width=3, color="#72B7B2")))
    if weights["kings"] > 0 and not kings.empty:
        inv_fig.add_trace(go.Scatter(x=kings["year"], y=kings["net_value"].map(to_display), name="Dividend Kings (after tax)", line=dict(width=3)))
    if weights["common"] > 0 and not common.empty:
        inv_fig.add_trace(go.Scatter(x=common["year"], y=common["net_value"].map(to_display), name="Common stocks (after tax)", line=dict(width=3)))
    if weights["roce"] > 0 and not roce.empty:
        inv_fig.add_trace(go.Scatter(x=roce["year"], y=roce["net_value"].map(to_display), name="ROCE / quality (after tax)", line=dict(width=3)))
    if xs:
        inv_fig.add_trace(go.Scatter(x=xs, y=[to_display(v) for v in net_line], name="Combined after-tax value", line=dict(width=4, color="#FFFFFF")))
        inv_fig.add_trace(go.Scatter(x=xs, y=[to_display(v) for v in contrib_line], name="Cumulative contributions", line=dict(width=2, dash="dot", color="#9D755D")))
        inv_fig.add_trace(go.Scatter(x=xs, y=[to_display(v) for v in tax_line], name="Tax paid / reserved", line=dict(width=2, dash="dash", color="#E45756")))
    inv_fig.update_layout(
        title="After-tax sleeves vs money you put in vs tax",
        xaxis_title="Years", yaxis_title=currency_label, hovermode="x unified",
    )
    inv_l, inv_r = st.columns([1.6, 1], vertical_alignment="top")
    with inv_l:
        plot_money(inv_fig, snap="Investment sleeves")
    with inv_r:
        advice_box(
            "How to read this tab",
            [
                f"You already hold **{money(existing_investments)}**. Monthly adding **{money(monthly_investments)}** ({money(monthly_investments * 12)} / year) from the sidebar.",
                "Dotted brown = cash you contributed (existing + monthly). Solid coloured = after-tax value of each sleeve. Dashed red = tax paid or reserved (41% deemed/exit on ETFs, 33% on share dividends/CGT).",
                "Cash in the bank is **not** this pot — set that on the master graph.",
                f"End of horizon: pot **{money(mix_end)}**, tax accounted **{money(mix_tax)}**.",
                "ETF 8-year deemed disposal is why the ETF line can step down even if you never sell.",
            ],
        )

    if extra_overpay > 0:
        st.caption(
            f"Housing tab extra repayment is {money(extra_overpay)} / month. That only affects the loan, not these sleeves."
        )

# ---------------------------------------------------------------------------
# Ventures — business and rental
# ---------------------------------------------------------------------------
with ventures_tab:
    st.subheader("Ventures: business and rental property")
    st.caption(
        "Irish tax here is simplified. A company pays 12.5% corporation tax on trading profit; taking cash out as salary/dividends is extra tax. "
        "A sole trader’s profit is stacked on income tax/USC/PRSI. Rent is taxed as income after costs; selling is 33% CGT. "
        "These pages always calculate. They only hit the **master projection** when you turn **Business** / **Rental property** on "
        "beside the master graph (both start **off**)."
    )
    st.caption(
        f"Currently in the master plan: business **{'on' if include_business else 'off'}**, "
        f"rental **{'on' if include_rental else 'off'}**."
    )

    st.markdown("**1. Start a business**")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        biz_start = date_field("Start date", date(planning_start.year + 1, 1, 1), key="biz_start")
    with b2:
        biz_capital = st.number_input("Cash you put in (€)", min_value=0.0, value=10_000.0, step=1_000.0)
        note("Seed from savings. Not tax-deductible as a gift to yourself; company share capital is locked in.")
    with b3:
        biz_loss_years = st.slider("Years until it makes a profit", 0, 8, 2)
        note("Many small firms take 1–3 years. During this we assume a small operating loss / draw.")
    with b4:
        structure = st.radio("Structure", ["Limited company (12.5% CT)", "Sole trader (income tax)"], index=0)

    biz_scale = st.slider("Years to scale to that steady profit (after the loss years)", 1, 10, 4)
    note(
        "A real start-up rarely prints the steady profit on day one of year 3. "
        "We ramp linearly from €0 to your steady profit over these extra years. Toggle **Business** beside the master graph to drop this whole line from the plan."
    )

    b5, b6, b7 = st.columns(3)
    with b5:
        biz_loss = st.number_input("Cash burn / year before profit (€)", min_value=0.0, value=5_000.0, step=500.0)
        note("Tools, insurance, accounting, a bit of marketing.")
    with b6:
        biz_profit = st.number_input("Steady profit / year after that (€)", min_value=0.0, value=20_000.0, step=1_000.0)
        note("Profit *before* owner pay. Be conservative.")
    with b7:
        extract_pct = st.slider("% of company profit taken out as salary/dividend", 0, 100, 50, 5)
        note("Leaving profit in a Ltd defers personal tax. Taking it out: PAYE or 40%+ USC on dividends.")

    biz_rows = []
    biz_cash = -biz_capital
    cum_tax = 0.0
    for offset in range(time_horizon_years):
        yr = planning_start.year + offset
        live = yr >= biz_start.year
        year_index = yr - biz_start.year
        profit = 0.0
        tax = 0.0
        owner = 0.0
        if live:
            if year_index < biz_loss_years:
                profit = -biz_loss
                biz_cash += profit
            else:
                grown = min(1.0, (year_index - biz_loss_years + 1) / max(biz_scale, 1))
                profit = biz_profit * grown
                if structure.startswith("Limited"):
                    ct = max(profit, 0.0) * 0.125
                    post_ct = profit - ct
                    taken = post_ct * extract_pct / 100
                    # ~52% personal on extraction (indicative higher-rate PAYE/dividend)
                    personal = taken * 0.52
                    tax = ct + personal
                    owner = taken - personal
                    biz_cash += post_ct - taken
                    cum_tax += tax
                else:
                    # sole trader: tax profit through USC/IT/PRSI ~52% above the band
                    tax = max(profit, 0.0) * 0.52
                    owner = profit - tax
                    biz_cash += 0.0
                    cum_tax += tax
        biz_rows.append({"year": yr, "profit": profit, "tax": tax, "owner_cash": owner, "retained": biz_cash})
    biz = pd.DataFrame(biz_rows)
    owner_total = float(biz["owner_cash"].sum())
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Cash you put in", money(biz_capital))
    v2.metric("Owner cash taken over horizon", money(owner_total))
    v3.metric("Tax paid (CT + personal)", money(float(biz["tax"].sum())))
    v4.metric("Value retained in the firm", money(float(biz["retained"].iloc[-1])))
    biz_fig = go.Figure()
    biz_fig.add_trace(go.Bar(name="Owner cash (after tax)", x=biz["year"], y=biz["owner_cash"].map(to_display), marker_color="#54A24B"))
    biz_fig.add_trace(go.Bar(name="Tax", x=biz["year"], y=biz["tax"].map(to_display), marker_color="#E45756"))
    biz_fig.add_trace(go.Scatter(name="Retained in firm", x=biz["year"], y=biz["retained"].map(to_display), line=dict(width=3)))
    biz_fig.update_layout(
        barmode="stack", title="Business: after-tax cash vs tax",
        xaxis_title="Calendar year", yaxis_title=currency_label, yaxis_tickformat=tick, hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=70, b=20),
    )
    plot_money(biz_fig, snap="Business venture")

    st.markdown("**2. Buy a rental property**")
    st.caption(
        f"Master-graph toggle: rental is **{'on' if include_rental else 'off'}**. "
        "Turn it off beside the master graph if you only want to explore the numbers here."
    )
    st.markdown("**Indicative Irish BTL / investment-property rates**")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Lender": r["lender"],
                    "c. 30% deposit": f"{r['ltv30']:.2f}%",
                    "c. 40% deposit": f"{r['ltv40']:.2f}%",
                    "Note": r["note"],
                }
                for r in IRISH_BTL
            ]
        ),
        hide_index=True, width="stretch",
    )
    note("BTL is usually 1.2–2.0pp dearer than owner-occupier, 30%+ deposit, and rental cover is stress-tested. Not a quote.")

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        rent_date = date_field("Purchase date", date(planning_start.year + 2, 3, 1), key="rent_date")
    with r2:
        rent_price = st.number_input("Purchase price (€)", min_value=0.0, value=250_000.0, step=5_000.0)
        note("Regional Ireland often €220k–350k; Dublin city much more.")
    with r3:
        rent_dep = st.slider("Deposit %", 10, 50, 30, 5)
        note("Buy-to-let deposits are often 30%+.")
    with r4:
        rent_rate = st.slider("BTL mortgage rate %", 2.0, 8.0, 5.35, 0.1)
        note("Default tracks a typical AIB-style 30% LTV BTL talking rate. Use the table above.")

    r5, r6, r7, r8 = st.columns(4)
    with r5:
        monthly_rent = st.number_input("Monthly rent (€)", min_value=0.0, value=1_500.0, step=50.0)
        note("Gross yield = rent × 12 / price. 5–8% is a common talking range before costs and tax.")
    with r6:
        occupancy = st.slider("Occupancy %", 70, 100, 95, 1)
        note("Allow voids and turnover. 5% empty is a modest assumption.")
    with r7:
        opex_pct = st.slider("Costs % of rent (ex-interest)", 10, 50, 25, 1)
        note("Insurance, agent, repairs, NPPR/LPT-type costs. Interest is modelled separately and is generally deductible.")
    with r8:
        growth = st.slider("House price growth % / year", -2.0, 8.0, 2.0, 0.1)

    hold_via = st.radio(
        "Hold the rental",
        ["Privately (income tax ~52% on profit)", "Irish Ltd (12.5% CT, then tax to take cash out)"],
        index=0,
        horizontal=True,
    )
    note(
        "Private: profit stacked on your PAYE (often ~52% above the band); 33% CGT on sale. "
        "Ltd: 12.5% CT inside the company, then ~52% to extract as salary/dividend. Close-company surcharge and s.23/s.97 rules are **not** modelled. Indicative only."
    )

    deposit = rent_price * rent_dep / 100
    loan_r = rent_price - deposit
    stamp_r = rent_price * 0.01
    payment_r = standard_payment(loan_r, rent_rate, 25)
    sched_r = amortize(loan_r, rent_rate, 25, 0.0)
    rent_rows = []
    cum_cash = -(deposit + stamp_r)
    for offset in range(time_horizon_years):
        yr = planning_start.year + offset
        live = yr >= rent_date.year
        yoi = yr - rent_date.year
        rent_in = monthly_rent * 12 * occupancy / 100 if live else 0.0
        opex = rent_in * opex_pct / 100
        interest = float(sched_r.loc[sched_r["year"] == yoi + 1, "interest"].sum()) if live and not sched_r.empty else 0.0
        if live and yoi + 1 > int(sched_r["year"].max() if not sched_r.empty else 0):
            interest = 0.0
        profit = rent_in - opex - interest
        finance_cost = (payment_r if live and loan_r > 0 else 0.0)
        if hold_via.startswith("Irish Ltd"):
            ct = max(profit, 0.0) * 0.125
            extract = max(profit - ct, 0.0) * 0.50
            personal = extract * 0.52
            tax = ct + personal
            cash = rent_in - opex - finance_cost - tax
        else:
            tax = max(profit, 0.0) * 0.52
            cash = rent_in - opex - finance_cost - tax
        if live:
            cum_cash += cash
        value = rent_price * ((1 + growth / 100) ** max(yoi, 0)) if live else 0.0
        bal = float(sched_r.loc[sched_r["year"] == min(yoi + 1, int(sched_r["year"].max())), "balance"].iloc[-1]) if live and not sched_r.empty else 0.0
        rent_rows.append(
            {
                "year": yr, "rent": rent_in, "tax": tax, "cash": cash if live else 0.0,
                "interest": interest if live else 0.0, "finance": finance_cost if live else 0.0,
                "equity": max(value - bal, 0.0) if live else 0.0, "value": value,
            }
        )
    rdf = pd.DataFrame(rent_rows)
    sale_value = float(rdf["value"].iloc[-1])
    sale_bal = loan_r  # overwritten below
    if not sched_r.empty:
        held = max(time_horizon_years - max(rent_date.year - planning_start.year, 0), 1)
        rowmatch = sched_r[sched_r["year"] == min(held, int(sched_r["year"].max()))]
        sale_bal = float(rowmatch["balance"].iloc[0]) if not rowmatch.empty else 0.0
    gain = max(sale_value - rent_price, 0.0)
    cgt = gain * 0.33
    equity_exit = sale_value - sale_bal - cgt
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Cash to buy (deposit + 1% stamp)", money(deposit + stamp_r))
    q2.metric("Gross yield", f"{(monthly_rent * 12 / rent_price):.1%}" if rent_price else "—")
    q3.metric("Income tax on rent over horizon", money(float(rdf["tax"].sum())))
    q4.metric("Equity after 33% CGT if sold at horizon", money(equity_exit))
    note(
        f"If you sold at the horizon: estimated price {money(sale_value)}, loan left {money(sale_bal)}, "
        f"CGT {money(cgt)} on the gain. Cash rent along the way is after 52% notional income tax on profit."
    )
    rent_fig = go.Figure()
    rent_fig.add_trace(go.Bar(name="Net cash from rent (after tax & mortgage)", x=rdf["year"], y=rdf["cash"].map(to_display), marker_color="#54A24B"))
    rent_fig.add_trace(go.Bar(name="Income / CT tax on rent", x=rdf["year"], y=rdf["tax"].map(to_display), marker_color="#E45756"))
    rent_fig.add_trace(go.Bar(name="Financing cost (repayment)", x=rdf["year"], y=rdf["finance"].map(to_display), marker_color="#9D755D"))
    rent_fig.add_trace(go.Scatter(name="Interest that year", x=rdf["year"], y=rdf["interest"].map(to_display), line=dict(width=2, dash="dot", color="#F58518")))
    rent_fig.add_trace(go.Scatter(name="Equity in the property", x=rdf["year"], y=rdf["equity"].map(to_display), line=dict(width=3)))
    rent_fig.update_layout(
        title="Rental: cash vs tax vs financing vs equity",
        xaxis_title="Calendar year", yaxis_title=currency_label, hovermode="x unified",
    )
    rv_l, rv_r = st.columns([1.55, 1], vertical_alignment="top")
    with rv_l:
        plot_money(rent_fig, snap="Rental property")
    with rv_r:
        cover = (monthly_rent * 12 * occupancy / 100) / (payment_r * 12) if payment_r else 0
        advice_box(
            "When (and how) to execute this rental",
            [
                f"Cash to buy is **{money(deposit + stamp_r)}**. If year-1 bank cash is tight on the master graph, delay the purchase date or raise the deposit from savings first.",
                f"Gross yield **{(monthly_rent * 12 / rent_price):.1%}**. Mortgage at **{rent_rate:.2f}%**. Rent / repayment cover ~ **{cover:.2f}×** (lenders often want >1.25× stressed).",
                "Private: simple, 52%-style tax on profit, 33% CGT on sale. Ltd: lower tax while profits sit in the company, painful to extract, extra accounting. One rental is usually held **privately** unless you are building a portfolio.",
                "Execute when: (1) owner-occupier mortgage is stable, (2) you can lose 6 months of rent without touching emergency cash, (3) the BTL stress rate still cash-flows.",
                "Toggle **Rental property** off beside the master graph to keep this as a sandbox.",
            ],
        )

# ---------------------------------------------------------------------------
# Automotive
# ---------------------------------------------------------------------------
with auto_tab:
    st.subheader("Automotive TCO")
    st.caption("Choose brand first, then model. Plug-in hybrids split petrol and electricity from electric range vs annual km.")
    top1, top2, top3 = st.columns(3)
    with top1:
        country = st.selectbox("Vehicle market", list(CAR_MARKETS.keys()), index=0)
    with top2:
        n_cars = st.slider("Cars in household", 1, 3, 1)
    with top3:
        default_replace = st.slider("Default replacement cycle (years)", 3, 15, 8)
    market = CAR_MARKETS[country]
    st.caption(
        market["note"]
        + f" Petrol {money(market['petrol'], 2)}/L · diesel {money(market['diesel'], 2)}/L · electricity {money(market['electricity'], 2)}/kWh."
    )

    default_brands = ["Toyota", "Toyota", "Toyota"]
    default_models = ["Toyota Yaris Cross Hybrid", "Toyota Yaris Cross Hybrid", "Toyota Yaris Cross Hybrid"]
    slots: list[dict] = []
    car_cols = st.columns(n_cars)
    for i in range(n_cars):
        with car_cols[i]:
            st.markdown(f"**Vehicle {comma(i + 1)}**")
            brand = st.selectbox("1. Brand", BRANDS, index=BRANDS.index(default_brands[i]) if i < 3 else 0, key=f"brand_{i}")
            filtered = [c for c in CARS if c["brand"] == brand]
            names = [c["name"] for c in filtered]
            fallback = default_models[i] if i < 3 and default_models[i] in names else names[0]
            model_name = st.selectbox("2. Model", names, index=names.index(fallback), key=f"model_{i}")
            car = next(c for c in CARS if c["name"] == model_name)
            fuel_note = car["fuel"].upper()
            if car["fuel"] == "phev":
                fuel_note += f" · electric range {comma(car['ev_range'])} km · {car['ice_use']} L/100 km on petrol · {car['kwh']} kWh/100 km"
            elif car["fuel"] == "ev":
                fuel_note += f" · {car['kwh']} kWh/100 km"
            else:
                fuel_note += f" · {car['ice_use']} L/100 km"
            st.caption(fuel_note)
            d1, d2, d3 = st.columns(3)
            with d1:
                buy_date = date_field(
                    "Target purchase date",
                    date(planning_start.year + i, min(3 + i * 4, 12), 1),
                    key=f"buy_{i}",
                )
            with d2:
                replace_years = st.slider("Replace every (years)", 3, 15, default_replace, key=f"rep_{i}")
            with d3:
                km = st.slider("Annual km", 5_000, 40_000, int(market["typical_km"]), 1_000, key=f"km_{i}")
            daily_km = km / 365
            weekly_km = km / 52
            st.caption(
                f"Mileage: **{comma(km)} km / year** = about **{daily_km:,.1f} km / day** or **{weekly_km:,.0f} km / week**."
            )
            if car["fuel"] == "phev":
                uf = phev_utility_factor(car["ev_range"], km)
                elec_km = km * uf
                ice_km = km - elec_km
                petrol_e, elec_e, _ = energy_cost(car, market, km)
                st.info(
                    f"**Plug-in hybrid:** official electric range {comma(car['ev_range'])} km. "
                    f"With this mileage we assume **{uf:.0%} of km on electric** "
                    f"({elec_km:,.0f} km electric / {ice_km:,.0f} km on petrol). "
                    f"Year-1 energy: petrol {money(petrol_e)}, electricity {money(elec_e)}. "
                    "Short commutes (under the electric range) stay mostly electric; long weekly motorway miles burn petrol."
                )
            elif car["fuel"] == "ev":
                st.caption("Battery EV: all of these km are modelled on electricity (no petrol line).")
            pack = dealer_pack(brand, model_name)
            st.markdown("**How you pay for it**")
            finance = st.selectbox(
                "Purchase method",
                ["Hire purchase (HP)", "PCP (dealer balloon)", "Cash (pay the OTR price)"],
                index=0, key=f"fin_mode_{i}",
            )
            note(pack["note"])
            st.caption(f"{pack['captive']}: typical HP {pack['hp_apr']:.1f}% APR · PCP {pack['pcp_apr']:.1f}% APR · deposit ~{pack['deposit_pct']:.0f}% · PCP balloon ~{pack['balloon_pct']:.0f}% of OTR.")
            if finance.startswith("Cash"):
                apr = dep_pct = term = balloon_pct = 0.0
            else:
                f1, f2, f3, f4 = st.columns(4)
                with f1:
                    default_apr = pack["pcp_apr"] if "PCP" in finance else pack["hp_apr"]
                    apr = st.slider("APR %", 0.0, 16.0, float(default_apr), 0.1, key=f"fin_apr_{i}")
                    note("Irish dealer campaign ranges, not a personal quote. Your rate moves with credit score and offer month.")
                with f2:
                    dep_pct = st.slider("Deposit %", 0, 50, int(pack["deposit_pct"]), 1, key=f"fin_dep_{i}")
                with f3:
                    default_term = pack["pcp_term"] if "PCP" in finance else pack["hp_term"]
                    term = st.slider("Finance term (years)", 2, 8, int(default_term), key=f"fin_term_{i}")
                with f4:
                    balloon_pct = st.slider(
                        "PCP balloon % of OTR", 0, 55, int(pack["balloon_pct"]), 1,
                        key=f"fin_bal_{i}", disabled="PCP" not in finance,
                    )
                    note("GMFV/balloon is due at the end unless you hand the car back or refinance. HP has no balloon.")
            slots.append(
                {
                    "label": f"Vehicle {comma(i + 1)}", "car": car, "buy_date": buy_date,
                    "replace_years": replace_years, "km": km, "finance": finance,
                    "apr": apr, "deposit_pct": dep_pct, "term": term, "balloon_pct": balloon_pct if "PCP" in finance else 0.0,
                }
            )

    fleet, summaries = fleet_timeline(slots, market, planning_start, time_horizon_years)
    household_tco = float(fleet["cum_tco"].iloc[-1]) if not fleet.empty else 0.0
    residual = float(summaries["Residual at horizon"].sum()) if not summaries.empty else 0.0
    m1, m2, m3 = st.columns(3)
    m1.metric("Household TCO to horizon", money(household_tco))
    m2.metric("Residual value still held", money(residual))
    m3.metric("TCO minus residual still held", money(household_tco - residual))
    note(
        "**TCO (total cost of ownership)** is the economic cost of having the cars: depreciation + fuel + tyres, service, "
        "NCT, tax, insurance and repairs. It is **not** the dealer finance monthly. "
        "The finance monthly is only the HP/PCP repayment. Cash purchase has no finance monthly."
    )

    if not summaries.empty:
        show = summaries.copy()
        show = show.rename(columns={"Monthly (indicative)": "Finance monthly (HP/PCP)"})
        show["Horizon TCO"] = show["Horizon TCO"].map(money)
        show["Residual at horizon"] = show["Residual at horizon"].map(money)
        show["Finance monthly (HP/PCP)"] = show["Finance monthly (HP/PCP)"].map(money)
        st.dataframe(show, hide_index=True, width="stretch")

    fleet_fig = go.Figure()
    fleet_fig.add_trace(go.Bar(name="Depreciation", x=fleet["calendar_year"], y=fleet["depreciation"].map(to_display), marker_color="#4C78A8"))
    fleet_fig.add_trace(go.Bar(name="Fuel / energy", x=fleet["calendar_year"], y=fleet["energy"].map(to_display), marker_color="#54A24B"))
    fleet_fig.add_trace(go.Bar(name="Tyres / service / NCT", x=fleet["calendar_year"], y=(fleet["tyres"] + fleet["service"] + fleet["nct"]).map(to_display), marker_color="#F58518"))
    fleet_fig.add_trace(go.Bar(name="Tax + insurance", x=fleet["calendar_year"], y=(fleet["tax"] + fleet["insurance"]).map(to_display), marker_color="#B279A2"))
    fleet_fig.add_trace(go.Bar(name="Repairs", x=fleet["calendar_year"], y=fleet["maintenance"].map(to_display), marker_color="#9D755D"))
    fleet_fig.add_trace(go.Bar(name="Deposit / cash buy / sale", x=fleet["calendar_year"], y=fleet["cash_capex"].map(to_display), marker_color="#E45756"))
    fleet_fig.add_trace(go.Bar(name="Finance repayments", x=fleet["calendar_year"], y=fleet["finance_pay"].map(to_display), marker_color="#FF9DA6"))
    fleet_fig.add_trace(go.Scatter(
        name="Cumulative household TCO", x=fleet["calendar_year"], y=fleet["cum_tco"].map(to_display),
        mode="lines+markers", line=dict(width=3), yaxis="y2",
    ))
    fleet_fig.update_layout(
        barmode="relative", title="Household fleet costs by calendar year",
        xaxis_title="Calendar year", yaxis_title=f"Annual ({cur})",
        yaxis2=dict(title=f"Cumulative ({cur})", overlaying="y", side="right", tickformat=tick),
        yaxis_tickformat=tick, hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=70, b=20),
    )
    plot_money(fleet_fig, snap="Household cars")
    if not fleet.empty:
        cash_view = fleet[["calendar_year", "energy", "standing", "maintenance", "finance_pay", "cash_capex", "cash_cars"]].copy()
        cash_view["calendar_year"] = cash_view["calendar_year"].map(int)
        for col in ("energy", "standing", "maintenance", "finance_pay", "cash_capex", "cash_cars"):
            cash_view[col] = cash_view[col].map(money)
        cash_view = cash_view.rename(columns={
            "calendar_year": "Year",
            "energy": "Fuel / energy",
            "standing": "Tax, insurance, tyres, NCT, service",
            "maintenance": "Repairs",
            "finance_pay": "Finance repayments",
            "cash_capex": "Deposit / cash buy / sale",
            "cash_cars": "Cash out for cars that year",
        })
        st.caption("Absolute cash amounts by year (not depreciation). Negative deposit/sale is money back in from selling.")
        st.dataframe(cash_view, hide_index=True, width="stretch")

    first = slots[0]
    tco = project_vehicle_tco(first["car"], market, first["replace_years"], first["km"])
    end_tco = tco.iloc[-1]
    purchase = float(end_tco["purchase"])
    resale = float(end_tco["resale"])
    net_tco = float(end_tco["net_tco"])
    v1, v2, v3, v4, v5 = st.columns(5)
    v1.metric("Upfront purchase", money(purchase))
    v2.metric("Petrol in this cycle", money(tco["petrol"].sum()))
    v3.metric("Electricity in this cycle", money(tco["electricity"].sum()))
    if first["car"]["fuel"] == "phev":
        v4.metric("Share of km on electric", f"{end_tco['ev_share']:.0%}")
    else:
        v4.metric("Tax + insurance / year (yr 1)", money(float(tco.iloc[0]["tax"] + tco.iloc[0]["insurance"])))
    v5.metric("Net cost this cycle", money(net_tco))

    brk = go.Figure(go.Bar(
        x=["Depreciation", "Petrol", "Electricity", "Tyres", "Servicing", "NCT", "Motor tax", "Insurance", "Repairs"],
        y=[
            to_display(end_tco["cum_depreciation"]),
            to_display(tco["petrol"].sum()), to_display(tco["electricity"].sum()),
            to_display(tco["tyres"].sum()), to_display(tco["service"].sum()),
            to_display(tco["nct"].sum()), to_display(tco["tax"].sum()),
            to_display(tco["insurance"].sum()), to_display(tco["maintenance"].sum()),
        ],
        marker_color="#4C78A8",
    ))
    brk.update_layout(
        title=f"{first['car']['name']}: this ownership cycle cost stack",
        yaxis_title=cur, yaxis_tickformat=tick, showlegend=False, margin=dict(l=20, r=20, t=50, b=20),
    )
    plot_money(brk)

# ---------------------------------------------------------------------------
# Family
# ---------------------------------------------------------------------------
with family_tab:
    st.subheader("Family, education & human capital")
    st.caption(
        "This tab is the children’s costs only. Parents’ courses, MBAs and earning-upside sit on Earners. "
        "College is split into tuition/fees, rent, and pocket money — rent applies only if that child lives away."
    )
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        n_children = st.slider("Number of children", 0, 6, 0)
    with f2:
        childcare_until = st.slider("Childcare until age", 0, 8, 5)
        note("ECCE preschool often from ~2 years 8 months; many use paid care until 4–5.")
    with f3:
        default_leave = st.slider("Parental leave before paid childcare (months)", 0, 24, 9)
        note("Ireland typical stack: maternity 26 weeks + parent's leave 9 weeks each + paternity 2 weeks. 6–12 months before creche is common.")
    with f4:
        uni_years = st.slider("College duration (years)", 1, 6, 4)
        note("Most Irish undergrad 3–4 years; some courses 5.")

    children: list[dict] = []
    if n_children:
        child_cols = st.columns(min(n_children, 3))
    for i in range(n_children):
        with child_cols[i % 3]:
            st.markdown(f"**Child {comma(i + 1)}**")
            a, b, c = st.columns(3)
            with a:
                birth = date_field("Birth date", date(planning_start.year - 5, 1, 1), key=f"birth_{i}")
            with b:
                college = st.checkbox("Plans to attend college", value=False, key=f"col_{i}")
            with c:
                college_start = date_field(
                    "College start date", date(birth.year + 18, 9, 1), key=f"colstart_{i}", disabled=not college,
                )
            d, e = st.columns(2)
            with d:
                lives_away = st.checkbox(
                    "Lives away during college (rent applies)",
                    value=True, key=f"away_{i}", disabled=not college,
                )
                note("Uncheck if they stay at home — rent is then €0. Fees and pocket money still apply.")
            with e:
                post_college = st.checkbox(
                    "Help with costs after college",
                    value=False, key=f"post_{i}", disabled=not college,
                )
                note("Optional extra years after graduation (first job, master’s). This is not school or college.")
            leave_m = st.slider(
                "Leave before this child's paid childcare (months)",
                0, 24, default_leave, key=f"leave_{i}",
            )
            note(
                f"Paid childcare for Child {comma(i + 1)} starts {comma(leave_m)} months after {irish_date(birth)} "
                f"(from {irish_date(date(birth.year + (birth.month + leave_m - 1) // 12, (birth.month + leave_m - 1) % 12 + 1, min(birth.day, 28)))})."
            )
            children.append(
                {
                    "birth": birth, "college": college, "college_start": college_start,
                    "leave_months": leave_m, "lives_away": lives_away, "post_college": post_college,
                }
            )

    band = st.selectbox(
        "Childcare cost band (typical Ireland, per child)",
        list(CHILDCARE_BANDS.keys()),
        index=2,
    )
    note(
        "Full-time creche is often €800–1,100/month outside Dublin and €1,100–1,400 in Dublin. "
        "Part-time ~€400–800. Childminders often €5–8/hour. NCS can reduce the net fee."
    )
    band_value = CHILDCARE_BANDS[band]
    if band_value is None:
        childcare_monthly = st.number_input(
            "Custom childcare / child / month (€)", min_value=0.0, value=1_100.0, step=50.0, format=MONEY_FMT,
        )
    else:
        childcare_monthly = band_value
        st.metric("Childcare used in the model", money(childcare_monthly) + " / month / child")

    st.markdown("**Clothes, school and general child spend (only while they are that age)**")
    cs1, cs2 = st.columns([2, 1])
    with cs1:
        child_annual = banded_euro(
            "Clothes / school / activities / year per child",
            CHILD_COST_BANDS, "Typical clothes, school, activities (~€4,500)",
            "Uniforms, shoes, books, sports, extra food — not creche and not college. This stops when they reach the age on the right.",
            "child_cost_band", 4_500.0,
        )
    with cs2:
        child_until = st.slider("Pay this until age", 12, 22, 18, key="child_until_age")
        note("Default 18: it drops off after school. College is a separate line below.")
    st.caption(
        f"Each child costs **{money(child_annual)} / year** from birth until the June they turn **{comma(child_until)}**. "
        "After that this line is €0 for that child (college fees/rent/pocket still apply if ticked)."
    )

    st.markdown("**College costs per attending child / year**")
    st.caption("Defaults are typical Irish public-college averages. Change the band if they go abroad or live differently.")
    u1, u2, u3 = st.columns(3)
    with u1:
        uni_fees = banded_euro(
            "Tuition / student contribution",
            UNI_FEE_BANDS, "Irish student contribution (~€3,000)",
            "Most Irish undergrads pay the student contribution (~€3,000), not full fees. UK/EU/US bands are much higher.",
            "uni_fee_band", 3_000.0,
        )
    with u2:
        uni_rent = banded_euro(
            "Rent if they live away",
            UNI_RENT_BANDS, "Away from home, typical (~€7,200)",
            "9–12 months of student housing. Regional shared houses often €400–550/month; Dublin €700–1,000+. €0 if they live at home.",
            "uni_rent_band", 7_200.0,
        )
    with u3:
        uni_pocket = banded_euro(
            "Pocket money / living (food, bus, social)",
            UNI_POCKET_BANDS, "Typical student (~€3,600)",
            "On top of rent and fees. ~€200–300/month lean; ~€300–450 typical; more if they don’t cook or commute far.",
            "uni_pocket_band", 3_600.0,
        )

    st.markdown("**Optional support after college**")
    st.caption(
        "Not a ‘career spend’ budget. Use this only if you will still help after they finish the degree "
        "(for example rent while they start a job). Parents’ own training is on Earners. Default is none."
    )
    s1, s2 = st.columns(2)
    with s1:
        support_annual = banded_euro(
            "Help after college / year",
            POST_COLLEGE_BANDS, "None — they cover themselves (€0)",
            "Light help ~€3,000–5,000; covering a room ~€6,000–9,000. Tick ‘Help with costs after college’ on the child.",
            "post_college_band", 4_000.0,
        )
    with s2:
        support_years = st.slider("Years of help after they graduate", 0, 6, 2)
        note("Only used when a child has the after-college box ticked and the amount is not €0.")

    fam = family_timeline(
        start=planning_start, years=time_horizon_years, children=children,
        childcare_until=childcare_until, childcare_monthly=childcare_monthly,
        child_annual=child_annual, child_until=child_until, uni_years=uni_years,
        uni_fees=uni_fees, uni_rent=uni_rent, uni_pocket=uni_pocket,
        support_annual=support_annual, support_years=support_years,
    )
    fam_end = float(fam["cumulative"].iloc[-1]) if not fam.empty else 0.0
    p1, p2, p3, p4 = st.columns(4)
    p1.metric(f"Cumulative family spend ({comma(time_horizon_years)}y)", money(fam_end))
    p2.metric("Peak year spend", money(float(fam["total"].max()) if not fam.empty else 0))
    p3.metric("College total (fees + rent + pocket)", money(float(fam["university"].sum()) if not fam.empty else 0))
    p4.metric("After-college help total", money(float(fam["post_college"].sum()) if not fam.empty else 0))
    if not fam.empty:
        note(
            f"Of college: fees {money(float(fam['uni_fees'].sum()))} · "
            f"rent {money(float(fam['uni_rent'].sum()))} · "
            f"pocket money {money(float(fam['uni_pocket'].sum()))}."
        )

    fam_fig = go.Figure()
    fam_fig.add_trace(go.Bar(name="Childcare", x=fam["year"], y=fam["childcare"].map(to_display), marker_color="#F58518"))
    fam_fig.add_trace(go.Bar(name="Clothes / school / activities", x=fam["year"], y=fam["child_costs"].map(to_display), marker_color="#4C78A8"))
    fam_fig.add_trace(go.Bar(name="College fees", x=fam["year"], y=fam["uni_fees"].map(to_display), marker_color="#54A24B"))
    fam_fig.add_trace(go.Bar(name="College rent", x=fam["year"], y=fam["uni_rent"].map(to_display), marker_color="#72B7B2"))
    fam_fig.add_trace(go.Bar(name="Pocket money", x=fam["year"], y=fam["uni_pocket"].map(to_display), marker_color="#B279A2"))
    fam_fig.add_trace(go.Bar(name="Help after college", x=fam["year"], y=fam["post_college"].map(to_display), marker_color="#E45756"))
    fam_fig.add_trace(go.Scatter(name="Cumulative", x=fam["year"], y=fam["cumulative"].map(to_display), mode="lines", line=dict(width=3), yaxis="y2"))
    fam_fig.update_layout(
        barmode="stack", title="Family spend by calendar year", xaxis_title="Calendar year",
        yaxis_title=f"Annual spend ({cur})", yaxis_tickformat=tick, yaxis_hoverformat=tick,
        yaxis2=dict(title=f"Cumulative ({cur})", overlaying="y", side="right", tickformat=tick),
        hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=70, b=20),
    )
    plot_money(fam_fig, snap="Family and college")

# ---------------------------------------------------------------------------
# Lifestyle
# ---------------------------------------------------------------------------
with lifestyle_tab:
    st.subheader("Lifestyle allowances")
    st.caption("Food, clothing, holidays and hobbies. Amounts inflate from the planning start date.")
    l1, l2, l3, l4 = st.columns(4)
    with l1:
        food_m = st.number_input("Food / month (€)", min_value=0.0, value=800.0, step=25.0, format=MONEY_FMT)
        note("Groceries, household of 2–4: often €500–800 modest; €800–1,200 typical; €1,400+ plenty of extras.")
    with l2:
        clothes_m = st.number_input("Clothing / month (€)", min_value=0.0, value=100.0, step=10.0, format=MONEY_FMT)
        note("Adults ~€50–150 each; kids grow fast ~€40–100.")
    with l3:
        holiday_adults = st.number_input(
            "Holidays / year — adults only (€)", min_value=0.0, value=2_000.0, step=250.0, format=MONEY_FMT,
        )
        note("Couple, week in Europe ~€1,500–3,000; long-haul more. Used in years with no child under 18 at home.")
    with l4:
        holiday_family = st.number_input(
            "Holidays / year — with children (€)", min_value=0.0, value=4_000.0, step=250.0, format=MONEY_FMT,
        )
        note("Family of 3–4, week in Europe ~€3,500–7,000. Used while any child is under 18.")
    l5, l6, l7 = st.columns(3)
    with l5:
        hobby_m = st.number_input("Hobbies / month (€)", min_value=0.0, value=100.0, step=10.0, format=MONEY_FMT)
        note("Gym €40–70; clubs/sports €20–80; a serious hobby can be €150–400.")
    with l6:
        eating_out_m = st.number_input("Eating out / month (€)", min_value=0.0, value=150.0, step=10.0, format=MONEY_FMT)
        note("A couple of casual meals: ~€80–150; regular dining out €250–500.")
    with l7:
        inflate = st.slider("Lifestyle inflation (% / year)", 0.0, 8.0, 2.5, 0.1)
        note("Ireland CPI has often sat ~2–3% in calm years; food can run hotter.")

    st.markdown("**Medical and other lifetime costs people forget**")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        med_ins = st.number_input("Private health insurance / year (€)", min_value=0.0, value=2_000.0, step=100.0, format=MONEY_FMT)
        note("VHI/Laya/Irish Life: ~€1,000–1,800 per adult; family plans often €2,400–4,500. Employer-paid cover can be a BIK on Earners.")
    with m2:
        med_oop = st.number_input("GP / dentist / pharmacy / year (€)", min_value=0.0, value=500.0, step=50.0, format=MONEY_FMT)
        note("Even with insurance: excesses, dentist, physio, glasses. €500–1,500 is a common household plug.")
    with m3:
        life_ins = st.number_input("Life / specified-illness / income protection / year (€)", min_value=0.0, value=600.0, step=50.0, format=MONEY_FMT)
        note("Mortgage protection is often required. Family income protection is extra.")
    with m4:
        other_life = st.number_input("Phone / streaming / pets / gifts / year (€)", min_value=0.0, value=1_200.0, step=50.0, format=MONEY_FMT)
        note("Two mobiles + TV + Christmas + a dog add up. Use this as a catch-all.")
    st.caption(
        "Also already in other tabs: LPT, utilities, broadband (Housing); cars (Cars); college (Family); "
        "pension (Earners). Still worth a separate think: **care for parents**, **funeral**, **wedding**, **emergency fund** "
        "(3–6 months of costs), **will/solicitor**, **professional subs**, **child activities** if not in the child-cost band."
    )

    life_rows = []
    cum = 0.0
    for offset in range(time_horizon_years):
        factor = (1 + inflate / 100) ** offset
        yr = planning_start.year + offset
        food = food_m * 12 * factor
        clothes = clothes_m * 12 * factor
        as_of = date(yr, 6, 1)
        kids_home = any(0 <= age_on(as_of, c["birth"]) < 18 for c in children) if children else False
        holidays = (holiday_family if kids_home else holiday_adults) * factor
        hobbies = hobby_m * 12 * factor
        eating = eating_out_m * 12 * factor
        medical = (med_ins + med_oop + life_ins) * factor
        otherc = other_life * factor
        total = food + clothes + holidays + hobbies + eating + medical + otherc
        cum += total
        life_rows.append(
            {
                "year": yr, "food": food, "clothing": clothes, "holidays": holidays,
                "hobbies": hobbies, "eating_out": eating, "medical": medical, "other": otherc,
                "kids_home": kids_home, "total": total, "cumulative": cum,
            }
        )
    life = pd.DataFrame(life_rows)
    z1, z2, z3 = st.columns(3)
    z1.metric("Year-1 lifestyle", money(float(life["total"].iloc[0]) if not life.empty else 0))
    z2.metric(f"Cumulative ({comma(time_horizon_years)}y)", money(float(life["cumulative"].iloc[-1]) if not life.empty else 0))
    z3.metric("Final-year lifestyle", money(float(life["total"].iloc[-1]) if not life.empty else 0))
    if not life.empty:
        n_fam = int(life["kids_home"].sum())
        note(
            f"Holiday budget uses the **with children** amount in {comma(n_fam)} years and the **adults only** amount in the rest, "
            "based on whether any child is under 18 that June."
        )

    life_fig = go.Figure()
    life_fig.add_trace(go.Bar(name="Food", x=life["year"], y=life["food"].map(to_display), marker_color="#54A24B"))
    life_fig.add_trace(go.Bar(name="Clothing", x=life["year"], y=life["clothing"].map(to_display), marker_color="#4C78A8"))
    life_fig.add_trace(go.Bar(name="Holidays", x=life["year"], y=life["holidays"].map(to_display), marker_color="#E45756"))
    life_fig.add_trace(go.Bar(name="Hobbies", x=life["year"], y=life["hobbies"].map(to_display), marker_color="#F58518"))
    life_fig.add_trace(go.Bar(name="Eating out", x=life["year"], y=life["eating_out"].map(to_display), marker_color="#B279A2"))
    life_fig.add_trace(go.Bar(name="Medical / protection", x=life["year"], y=life["medical"].map(to_display), marker_color="#E45756"))
    life_fig.add_trace(go.Bar(name="Other (phone, pets, gifts)", x=life["year"], y=life["other"].map(to_display), marker_color="#9D755D"))
    life_fig.add_trace(go.Scatter(name="Cumulative", x=life["year"], y=life["cumulative"].map(to_display), mode="lines", line=dict(width=3), yaxis="y2"))
    life_fig.update_layout(
        barmode="stack", title="Lifestyle spend by calendar year", xaxis_title="Calendar year",
        yaxis_title=f"Annual ({cur})", yaxis_tickformat=tick,
        yaxis2=dict(title=f"Cumulative ({cur})", overlaying="y", side="right", tickformat=tick),
        hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=20, r=20, t=70, b=20),
    )
    plot_money(life_fig, snap="Lifestyle")

# ---------------------------------------------------------------------------
# Overview charts (filled last so they see every tab’s inputs)
# ---------------------------------------------------------------------------
projection = project_finances(
    cash=plan_start_cash, monthly_contrib=monthly_investments, home=home_value,
    mortgage=mortgage_balance, years=time_horizon_years, invest_return=annual_return,
    loan_rate=mortgage_rate, monthly_payment=monthly_mortgage_payment,
    start_investments=float(st.session_state.existing_investments),
)
yearly = projection[projection["month"] % 12 == 0].copy()
yearly["calendar_year"] = planning_start.year + yearly["year"].round().astype(int)

spend_rows = []
asset_rows = []
cash_bal = plan_start_cash
peak_gap = 0.0
car_finance_used = any(not str(s.get("finance", "")).startswith("Cash") for s in slots)
for _, prow in yearly.iterrows():
    yr = int(prow["calendar_year"])
    last_year = yr >= planning_start.year + time_horizon_years
    apply_year = int(prow["month"]) > 0
    flow_year = yr - 1 if apply_year else yr
    mortgage_out = monthly_mortgage_payment * 12
    home_out = col_year(home_run, flow_year, "total")
    reno_out = sum(r["Net cost"] for r in reno_rows if r.get("year") == flow_year)
    life_out = col_year(life, flow_year, "total")
    fam_out = col_year(fam, flow_year, "total")
    car_run_cash = (
        col_year(fleet, flow_year, "maintenance", "calendar_year")
        + col_year(fleet, flow_year, "energy", "calendar_year")
        + col_year(fleet, flow_year, "standing", "calendar_year")
        + col_year(fleet, flow_year, "finance_pay", "calendar_year")
    )
    car_capex = col_year(fleet, flow_year, "cash_capex", "calendar_year")
    car_buy = max(car_capex, 0.0)
    car_sale = max(-car_capex, 0.0)
    biz_out = 0.0
    rent_deposit = 0.0
    if include_business:
        biz_out = max(-col_year(biz, flow_year, "profit"), 0.0)
        if flow_year == biz_start.year:
            biz_out += biz_capital
    if include_rental and flow_year == rent_date.year:
        rent_deposit = deposit + stamp_r
    spend = mortgage_out + home_out + reno_out + life_out + fam_out + car_run_cash + car_buy + biz_out + rent_deposit
    net_in = col_year(pay_df, flow_year, "net") + car_sale
    if include_business:
        net_in += col_year(biz, flow_year, "owner_cash")
    if include_rental:
        net_in += col_year(rdf, flow_year, "cash")
    gap_now = 0.0
    if apply_year:
        cash_bal = cash_bal + net_in - spend - monthly_investments * 12
        if cash_bal < 0:
            gap_now = -cash_bal
            peak_gap = max(peak_gap, gap_now)
            cash_bal = 0.0
        spend_rows.append(
            {
                "year": flow_year, "mortgage": mortgage_out, "home": home_out + reno_out,
                "lifestyle": life_out, "family": fam_out, "cars": car_run_cash + car_buy,
                "ventures": biz_out + rent_deposit, "investing": monthly_investments * 12,
                "total": spend, "gap": gap_now,
            }
        )
    pension = 0.0 if not apply_year else col_year(pay_df, yr, "pension_pots")
    rental_eq = col_year(rdf, yr, "equity") if include_rental else 0.0
    rental_val = col_year(rdf, yr, "value") if include_rental else 0.0
    rental_loan = max(rental_val - rental_eq, 0.0)
    biz_kept = max(col_year(biz, yr, "retained"), 0.0) if include_business else 0.0
    cars_held = residual if last_year else 0.0
    car_loans = col_year(fleet, yr, "loan_end", "calendar_year")
    illiquid = prow["home_value"] + pension + biz_kept + rental_eq + cars_held
    liquid = float(prow["investments"])
    liabilities = prow["mortgage_balance"] + rental_loan + car_loans
    total_assets = cash_bal + liquid + illiquid
    asset_rows.append(
        {
            "year": yr, "cash": cash_bal, "liquid": liquid, "illiquid": illiquid,
            "assets": total_assets, "liabilities": liabilities, "gap": gap_now,
            "net_worth": total_assets - liabilities,
        }
    )
assets_df = pd.DataFrame(asset_rows)
spend_df = pd.DataFrame(spend_rows)
today_a = assets_df.iloc[0]
end_a = assets_df.iloc[-1]

with overview:
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlock"]:has(> div [data-testid="stSlider"][aria-label*="Master timeframe"]) {
            background: var(--background-color);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("Master position")
    cash_hi, other_hi = st.columns([1.15, 2.85])
    with cash_hi:
        st.markdown(
            f"<div style='background:#1f3d2a;border:2px solid #54A24B;border-radius:12px;padding:14px 16px;'>"
            f"<div style='color:#a8e6bf;font-size:0.85rem;letter-spacing:0.04em;'>CURRENT CASH IN THE BANK</div>"
            f"<div style='color:#ffffff;font-size:2rem;font-weight:700;line-height:1.2;'>{money(today_a['cash'])}</div>"
            f"<div style='color:#cfe8d8;font-size:0.9rem;'>Starting cash this run: {money(plan_start_cash)}"
            f" ({'included' if include_starting_cash else 'toggled off'})</div></div>",
            unsafe_allow_html=True,
        )
    with other_hi:
        m3, m4, m5, m6 = st.columns(4)
        m3.metric("Liquid investments", money(today_a["liquid"]))
        m4.metric("Illiquid assets", money(today_a["illiquid"]))
        m5.metric("Mortgage + monthly repayment", money(mortgage_balance), delta=money(monthly_mortgage_payment) + " / month")
        m6.metric(
            f"Net worth ({comma(time_horizon_years)}y)",
            money(end_a["net_worth"]),
            delta=money(end_a["net_worth"] - today_a["net_worth"]),
        )
    st.caption(
        f"Mortgage: **{money(mortgage_balance)}** outstanding, **{money(monthly_mortgage_payment)} / month** "
        f"({money(monthly_mortgage_payment * 12)} / year) from the sidebar. "
        f"The Housing tab modelled loan is **{money(loan)}** at **{money(pay)} / month**. "
        f"Lifetime interest if you never overpay: **{money(base_interest)}**."
    )
    if peak_gap > 1:
        st.warning(
            f"This plan needs extra credit of up to {money(peak_gap)} in the tightest year. "
            "The bank line stays at €0.00 rather than going negative — debts you already have (mortgage, car finance, BTL) are on the liabilities line."
        )

    st.markdown(
        "<div style='background:#243524;border:2px solid #54A24B;border-radius:10px;padding:8px 12px 2px 12px;margin:8px 0 12px 0;'>"
        "<p style='color:#d4f5e0;margin:0;font-weight:700;'>Starting cash amount — type it here</p></div>",
        unsafe_allow_html=True,
    )
    st.number_input(
        "Starting cash amount (€)",
        min_value=0.0,
        step=1_000.0,
        format="%.2f",
        key="initial_cash",
        help="Click in the box and type the cash you already have, then press Enter. This is the green diamond on the graph.",
    )

    left, right = st.columns([1.7, 1], vertical_alignment="top")
    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=assets_df["year"], y=assets_df["cash"].map(to_display), name="Cash in the bank",
            line=dict(width=5, color="#54A24B"),
        ))
        fig.add_trace(go.Scatter(
            x=[int(assets_df["year"].iloc[0])], y=[to_display(plan_start_cash)],
            mode="markers+text", name="Starting cash",
            text=[money(plan_start_cash)], textposition="top center",
            marker=dict(size=14, color="#54A24B", symbol="diamond"),
        ))
        fig.add_trace(go.Scatter(x=assets_df["year"], y=assets_df["liquid"].map(to_display), name="Liquid investments", line=dict(width=3)))
        fig.add_trace(go.Scatter(x=assets_df["year"], y=assets_df["illiquid"].map(to_display), name="Illiquid assets", line=dict(width=3, dash="dot")))
        fig.add_trace(go.Scatter(x=assets_df["year"], y=assets_df["assets"].map(to_display), name="Total assets", line=dict(width=3)))
        fig.add_trace(go.Scatter(x=assets_df["year"], y=assets_df["liabilities"].map(to_display), name="Total liabilities", line=dict(width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=assets_df["year"], y=assets_df["net_worth"].map(to_display), name="Net worth", line=dict(width=3), fill="tozeroy"))
        retire_year = (
            planning_start.year + max(retirement_age - earner_rows[0]["age"], 0) if earner_rows else None
        )
        add_plan_markers(fig, planning_start.year, retire_year, plan_start_cash)
        fig.update_layout(
            title="Cash, liquid investments, illiquid assets, and debts",
            xaxis_title="Calendar year", yaxis_title=currency_label,
            hovermode="x unified",
            yaxis=dict(tickformat=",.2f", tickprefix=cur, exponentformat="none", nticks=12, showgrid=True, gridwidth=1, griddash="dot"),
            height=520,
        )
        plot_money(fig, snap="Master position")
    with right:
        st.markdown("**Beside this graph**")
        st.toggle("Include starting cash", key="include_starting_cash")
        st.toggle("Business", key="include_business")
        st.toggle("Rental property", key="include_rental")
        note(
            "Business and rental default **off**. Off = they are a sandbox on the Ventures tab and "
            "**do not** change Master cash, spend, assets or Snapshot. Turn a switch on only if you want that venture in the plan."
        )
        st.caption("Planner explainer — scroll inside this box")
        explainer_scroll(
            explain_plan(assets_df, spend_df, pay_df, float(today_a["cash"]), peak_gap, car_finance_used),
            height=320,
        )

    hz1, hz2 = st.columns(2)
    with hz1:
        st.slider(
            "Master timeframe (years)", min_value=10, max_value=80, key="master_horizon",
            help="How far the master tracker, pensions, family and other tabs project.",
        )
    with hz2:
        st.slider(
            "Retirement age (Irish State Pension is 66)", min_value=55, max_value=75, key="retirement_age",
        )

    st.subheader("Spending overview")
    s1, s2, s3 = st.columns(3)
    s1.metric("This year’s spend", money(float(spend_df["total"].iloc[0]) if not spend_df.empty else 0))
    s2.metric("Peak year", money(float(spend_df["total"].max())))
    s3.metric(f"Cumulative spend ({comma(time_horizon_years)}y)", money(float(spend_df["total"].sum())))
    note("Bars are cash out the door. The dotted line is money moved into investments (saving). The gold line is the investment pot balance.")

    spend_fig = go.Figure()
    spend_fig.add_trace(go.Bar(name="Mortgage", x=spend_df["year"], y=spend_df["mortgage"].map(to_display), marker_color="#E45756"))
    spend_fig.add_trace(go.Bar(name="Home", x=spend_df["year"], y=spend_df["home"].map(to_display), marker_color="#F58518"))
    spend_fig.add_trace(go.Bar(name="Lifestyle", x=spend_df["year"], y=spend_df["lifestyle"].map(to_display), marker_color="#54A24B"))
    spend_fig.add_trace(go.Bar(name="Family", x=spend_df["year"], y=spend_df["family"].map(to_display), marker_color="#4C78A8"))
    spend_fig.add_trace(go.Bar(name="Cars", x=spend_df["year"], y=spend_df["cars"].map(to_display), marker_color="#B279A2"))
    spend_fig.add_trace(go.Bar(name="Ventures", x=spend_df["year"], y=spend_df["ventures"].map(to_display), marker_color="#9D755D"))
    spend_fig.add_trace(go.Scatter(
        name="Investing (contributions)", x=spend_df["year"], y=spend_df["investing"].map(to_display),
        mode="lines+markers", line=dict(width=2, dash="dot", color="#F58518"),
    ))
    spend_fig.add_trace(go.Scatter(
        name="Investment pot balance", x=assets_df["year"], y=assets_df["liquid"].map(to_display),
        mode="lines", line=dict(width=3, color="#FFBF00"), yaxis="y2",
    ))
    spend_fig.add_trace(go.Scatter(
        name="Total spend", x=spend_df["year"], y=spend_df["total"].map(to_display),
        mode="lines+markers", line=dict(width=3, color="#4C78A8"),
    ))
    spend_fig.update_layout(
        barmode="stack", title="Household spending by calendar year",
        xaxis_title="Calendar year", yaxis_title=currency_label,
        yaxis_tickformat=tick, yaxis_hoverformat=tick, hovermode="x unified",
        yaxis2=dict(title="Investment pot", overlaying="y", side="right", tickformat=tick),
    )
    add_plan_markers(
        spend_fig, planning_start.year,
        planning_start.year + max(retirement_age - earner_rows[0]["age"], 0) if earner_rows else None,
        plan_start_cash,
    )
    plot_money(spend_fig, snap="Spending overview")

with snapshot_slot:
    if not SNAPSHOT_FIGS:
        st.info("Charts appear here after the other tabs have run.")
    else:
        st.subheader("Snapshot of major graphs")
        note("One chart per row so axis labels and legends do not sit on top of each other.")
        for i, (title, sfig) in enumerate(SNAPSHOT_FIGS):
            st.markdown(f"**{title}**")
            copy = go.Figure(sfig.to_plotly_json())
            format_money_fig(copy)
            copy.update_layout(
                height=520,
                margin=dict(l=100, r=100, t=80, b=130),
                legend=dict(
                    orientation="h", yanchor="top", y=-0.28, xanchor="left", x=0,
                    font=dict(size=11), bgcolor="rgba(0,0,0,0)",
                ),
                font=dict(size=13),
            )
            copy.update_yaxes(nticks=5, tickfont=dict(size=11), automargin=True, title_standoff=16)
            copy.update_xaxes(automargin=True, tickfont=dict(size=11), title_standoff=16)
            copy.update_annotations(font=dict(size=10), yshift=8)
            st.plotly_chart(copy, width="stretch", key=f"snapshot_{i}")
            st.divider()
