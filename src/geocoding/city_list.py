"""
Top 100 Indian cities by population, ranked per the 2011 Census
(Wikipedia: List of cities in India by population - the standard
reference basis most "2025/2026 estimate" sites derive from).

Tier labels are MY OWN convention, not an official government tier system
(there is no single official "popularity tier" - see our earlier research).
Rule used:
  Tier 1 = rank 1-46  (the official "Million Plus" cities, pop. > 1,000,000)
  Tier 2 = rank 47-75 (large, well-known cities, pop. ~450k-1M)
  Tier 3 = rank 76-100 (smaller but still nationally recognized cities)

State is included for context/disambiguation (India has multiple
same-named places in different states).
"""

CITIES = [
    # rank, name, state, tier  (lat/lon filled in by geocoding step)
    (1, "Mumbai", "Maharashtra", 1),
    (2, "Delhi", "Delhi", 1),
    (3, "Bengaluru", "Karnataka", 1),
    (4, "Hyderabad", "Telangana", 1),
    (5, "Ahmedabad", "Gujarat", 1),
    (6, "Chennai", "Tamil Nadu", 1),
    (7, "Kolkata", "West Bengal", 1),
    (8, "Surat", "Gujarat", 1),
    (9, "Pune", "Maharashtra", 1),
    (10, "Jaipur", "Rajasthan", 1),
    (11, "Lucknow", "Uttar Pradesh", 1),
    (12, "Kanpur", "Uttar Pradesh", 1),
    (13, "Nagpur", "Maharashtra", 1),
    (14, "Indore", "Madhya Pradesh", 1),
    (15, "Thane", "Maharashtra", 1),
    (16, "Bhopal", "Madhya Pradesh", 1),
    (17, "Visakhapatnam", "Andhra Pradesh", 1),
    (18, "Pimpri-Chinchwad", "Maharashtra", 1),
    (19, "Patna", "Bihar", 1),
    (20, "Vadodara", "Gujarat", 1),
    (21, "Ghaziabad", "Uttar Pradesh", 1),
    (22, "Ludhiana", "Punjab", 1),
    (23, "Agra", "Uttar Pradesh", 1),
    (24, "Nashik", "Maharashtra", 1),
    (25, "Faridabad", "Haryana", 1),
    (26, "Meerut", "Uttar Pradesh", 1),
    (27, "Rajkot", "Gujarat", 1),
    (28, "Kalyan-Dombivli", "Maharashtra", 1),
    (29, "Vasai-Virar", "Maharashtra", 1),
    (30, "Varanasi", "Uttar Pradesh", 1),
    (31, "Srinagar", "Jammu and Kashmir", 1),
    (32, "Chhatrapati Sambhajinagar", "Maharashtra", 1),
    (33, "Dhanbad", "Jharkhand", 1),
    (34, "Amritsar", "Punjab", 1),
    (35, "Navi Mumbai", "Maharashtra", 1),
    (36, "Prayagraj", "Uttar Pradesh", 1),
    (37, "Howrah", "West Bengal", 1),
    (38, "Ranchi", "Jharkhand", 1),
    (39, "Jabalpur", "Madhya Pradesh", 1),
    (40, "Gwalior", "Madhya Pradesh", 1),
    (41, "Coimbatore", "Tamil Nadu", 1),
    (42, "Vijayawada", "Andhra Pradesh", 1),
    (43, "Jodhpur", "Rajasthan", 1),
    (44, "Madurai", "Tamil Nadu", 1),
    (45, "Raipur", "Chhattisgarh", 1),
    (46, "Kota", "Rajasthan", 1),
    (47, "Chandigarh", "Chandigarh", 2),
    (48, "Guwahati", "Assam", 2),
    (49, "Solapur", "Maharashtra", 2),
    (50, "Hubli-Dharwad", "Karnataka", 2),
    (51, "Bareilly", "Uttar Pradesh", 2),
    (52, "Mysore", "Karnataka", 2),
    (53, "Moradabad", "Uttar Pradesh", 2),
    (54, "Gurgaon", "Haryana", 2),
    (55, "Aligarh", "Uttar Pradesh", 2),
    (56, "Jalandhar", "Punjab", 2),
    (57, "Tiruchirappalli", "Tamil Nadu", 2),
    (58, "Bhubaneswar", "Odisha", 2),
    (59, "Salem", "Tamil Nadu", 2),
    (60, "Mira-Bhayandar", "Maharashtra", 2),
    (61, "Thiruvananthapuram", "Kerala", 2),
    (62, "Bhiwandi", "Maharashtra", 2),
    (63, "Saharanpur", "Uttar Pradesh", 2),
    (64, "Gorakhpur", "Uttar Pradesh", 2),
    (65, "Guntur", "Andhra Pradesh", 2),
    (66, "Amravati", "Maharashtra", 2),
    (67, "Bikaner", "Rajasthan", 2),
    (68, "Noida", "Uttar Pradesh", 2),
    (69, "Jamshedpur", "Jharkhand", 2),
    (70, "Bhilai", "Chhattisgarh", 2),
    (71, "Warangal", "Telangana", 2),
    (72, "Cuttack", "Odisha", 2),
    (73, "Firozabad", "Uttar Pradesh", 2),
    (74, "Kochi", "Kerala", 2),
    (75, "Bhavnagar", "Gujarat", 2),
    (76, "Dehradun", "Uttarakhand", 3),
    (77, "Durgapur", "West Bengal", 3),
    (78, "Asansol", "West Bengal", 3),
    (79, "Nanded", "Maharashtra", 3),
    (80, "Kolhapur", "Maharashtra", 3),
    (81, "Ajmer", "Rajasthan", 3),
    (82, "Kalaburagi", "Karnataka", 3),
    (83, "Loni", "Uttar Pradesh", 3),
    (84, "Ujjain", "Madhya Pradesh", 3),
    (85, "Siliguri", "West Bengal", 3),
    (86, "Ulhasnagar", "Maharashtra", 3),
    (87, "Jhansi", "Uttar Pradesh", 3),
    (88, "Sangli", "Maharashtra", 3),
    (89, "Jammu", "Jammu and Kashmir", 3),
    (90, "Nellore", "Andhra Pradesh", 3),
    (91, "Mangalore", "Karnataka", 3),
    (92, "Belgaum", "Karnataka", 3),
    (93, "Jamnagar", "Gujarat", 3),
    (94, "Tirunelveli", "Tamil Nadu", 3),
    (95, "Malegaon", "Maharashtra", 3),
    (96, "Gaya", "Bihar", 3),
    (97, "Ambattur", "Tamil Nadu", 3),
    (98, "Jalgaon", "Maharashtra", 3),
    (99, "Udaipur", "Rajasthan", 3),
    (100, "Maheshtala", "West Bengal", 3),
]

print(f"Total cities defined: {len(CITIES)}")
print(f"Tier 1 (rank 1-46, pop > 1M):  {sum(1 for c in CITIES if c[3]==1)} cities")
print(f"Tier 2 (rank 47-75):           {sum(1 for c in CITIES if c[3]==2)} cities")
print(f"Tier 3 (rank 76-100):          {sum(1 for c in CITIES if c[3]==3)} cities")
