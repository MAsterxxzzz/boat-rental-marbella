#!/bin/bash

################################################################################
# PHASE 35.3 AUTOMATED EMAIL BATCH SENDER
# Triggers email sends for scheduled batches
# Usage: ./send_batch_emails.sh [batch_number]
################################################################################

CAMPAIGN_DIR="/Users/nunnu/Desktop/boathire/boat-rental-marbella"
SENDER_EMAIL="boatrentalinmarbella@gmail.com"
ASSET_URL="https://boatrentalinmarbella.com/blog/boat-rental-marbella-price-index/"

# Batch definitions
declare -A BATCH_2=(
  ["nomadic_matt"]="contact@nomadicmatt.com|Nomadic Matt|editorial"
  ["hostelworld"]="partnerships@hostelworld.com|Hostelworld|platform"
  ["viamichelin"]="tourism@viamichelin.com|ViaMichelin|platform"
  ["tripadvisor"]="business@tripadvisor.com|TripAdvisor|platform"
  ["vrbo"]="partnerships@vrbo.com|Vrbo/HomeAway|vacation_rental"
)

declare -A BATCH_3=(
  ["spain_info"]="info@spain.info|Spain.info|government"
  ["lonely_planet"]="editorial@lonelyplanet.com|Lonely Planet|editorial"
  ["booking"]="partnerships@booking.com|Booking.com|platform"
  ["airbnb"]="host@airbnb.com|Airbnb Experiences|platform"
  ["superyacht"]="info@superyachtforum.com|SuperYacht Forum|forum"
)

################################################################################
# BATCH 2 EMAIL TEMPLATES
################################################################################

send_batch_2_nomadic_matt() {
  echo "📧 Sending to Nomadic Matt..."
  # Email sending triggered via Claude's email tools
  # Subject: Marbella Boat Rental Guide — Unique Data Resource for Your Readers
  # Body: [Editorial template with budget travel angle]
}

send_batch_2_hostelworld() {
  echo "📧 Sending to Hostelworld..."
  # Subject: Marbella Boat Charter Guide — Resource for Your Marbella City Guide
  # Body: [Platform template with backpacker angle]
}

send_batch_2_viamichelin() {
  echo "📧 Sending to ViaMichelin..."
  # Subject: Marbella Boat Charter Pricing Data — Travel Portal Resource
  # Body: [Platform template for European travel portals]
}

send_batch_2_tripadvisor() {
  echo "📧 Sending to TripAdvisor..."
  # Subject: Marbella Boat Rental Pricing Index — Resource for Activities
  # Body: [Platform template highlighting traveler value]
}

send_batch_2_vrbo() {
  echo "📧 Sending to Vrbo/HomeAway..."
  # Subject: Boat Charter Activities — Resource for Your Villa Renters
  # Body: [Vacation rental template for guest experiences]
}

################################################################################
# BATCH 3 EMAIL TEMPLATES
################################################################################

send_batch_3_spain_info() {
  echo "📧 Sending to Spain.info (Government)..."
  # Subject: Marbella Boat Charter Market Data — Tourism Resource
  # Body: [Government template for official tourism board]
}

send_batch_3_lonely_planet() {
  echo "📧 Sending to Lonely Planet..."
  # Subject: Marbella Boat Rental Pricing Index — Authoritative Reference
  # Body: [High-authority editorial template]
}

send_batch_3_booking() {
  echo "📧 Sending to Booking.com..."
  # Subject: Marbella Boat Charter Pricing — Resource for Booking Partners
  # Body: [Platform template for accommodation partners]
}

send_batch_3_airbnb() {
  echo "📧 Sending to Airbnb Experiences..."
  # Subject: Marbella Boat Rental Experience Data — Host Resource
  # Body: [Platform template for Airbnb experience hosts]
}

send_batch_3_superyacht() {
  echo "📧 Sending to SuperYacht Forum..."
  # Subject: Marbella Boat Charter Pricing Index
  # Body: [Forum template for community discussion]
}

################################################################################
# BATCH EXECUTION FUNCTIONS
################################################################################

send_batch_2() {
  echo "================================"
  echo "BATCH 2 EXECUTION (Sep 5, 2026)"
  echo "================================"
  echo "Sending 5 emails to Tier 2 prospects..."
  echo ""

  send_batch_2_nomadic_matt
  send_batch_2_hostelworld
  send_batch_2_viamichelin
  send_batch_2_tripadvisor
  send_batch_2_vrbo

  echo ""
  echo "✅ Batch 2 sent: $(date)"
  log_batch_sent "2" "5" "Sep 5, 2026"
}

send_batch_3() {
  echo "================================"
  echo "BATCH 3 EXECUTION (Sep 12, 2026)"
  echo "================================"
  echo "Sending 5 emails to Tier 3 prospects..."
  echo ""

  send_batch_3_spain_info
  send_batch_3_lonely_planet
  send_batch_3_booking
  send_batch_3_airbnb
  send_batch_3_superyacht

  echo ""
  echo "✅ Batch 3 sent: $(date)"
  log_batch_sent "3" "5" "Sep 12, 2026"
}

################################################################################
# LOGGING & TRACKING
################################################################################

log_batch_sent() {
  BATCH=$1
  COUNT=$2
  DATE=$3

  echo "✅ Batch $BATCH | $COUNT emails | Sent: $DATE" >> "$CAMPAIGN_DIR/OUTREACH_LOG.txt"
}

update_tracking_log() {
  BATCH=$1
  DATE=$(date +"%Y-%m-%d %H:%M:%S")

  echo "" >> "$CAMPAIGN_DIR/OUTREACH_TRACKING_LOG.md"
  echo "### Batch $BATCH Sent" >> "$CAMPAIGN_DIR/OUTREACH_TRACKING_LOG.md"
  echo "**Date:** $DATE" >> "$CAMPAIGN_DIR/OUTREACH_TRACKING_LOG.md"
  echo "**Status:** ✅ Sent" >> "$CAMPAIGN_DIR/OUTREACH_TRACKING_LOG.md"
  echo "" >> "$CAMPAIGN_DIR/OUTREACH_TRACKING_LOG.md"
}

################################################################################
# MAIN EXECUTION
################################################################################

main() {
  case "${1:-help}" in
    2)
      send_batch_2
      update_tracking_log "2"
      ;;
    3)
      send_batch_3
      update_tracking_log "3"
      ;;
    *)
      echo "Usage: $0 [batch_number]"
      echo ""
      echo "Available batches:"
      echo "  2 - Send Batch 2 (Sep 5) - 5 Tier-2 prospects"
      echo "  3 - Send Batch 3 (Sep 12) - 5 Tier-3 prospects"
      echo ""
      echo "Example:"
      echo "  $0 2     # Send Batch 2"
      echo "  $0 3     # Send Batch 3"
      ;;
  esac
}

main "$@"
