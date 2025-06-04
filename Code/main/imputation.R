library(dplyr)
library(tidyr)
library(readr)
library(stringr)
library(haven)
library(lavaan)
library(labelled)
df_combined <- read.csv("/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/Data/pretpourtrain.csv")


# 1. Fit on the non-missing wages only
# df_train <- df_combined %>% filter(!is.na(weekly_pay))
# # 
# model <- lm("weekly_pay ~ age + factor(educ)*age + factor(ncdsid)", data = df_train)
# saveRDS(model, file = "/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/Data/linear_model_weekly_pay2.rds")
# 

# 2. Predict for everyone
model <- readRDS("/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/Data/linear_model_weekly_pay2.rds")
id_levels <- levels(model$model[["factor(ncdsid)"]])
# split: rows we CAN impute vs. rows we LEAVE as NA
df_ok   <- df_combined %>% filter(ncdsid %in% id_levels)
df_skip <- df_combined %>% filter(!(ncdsid %in% id_levels))

df_ok <- df_ok %>%
  mutate(weekly_pay = if_else(
    working_status == 0 & is.na(weekly_pay),
    0,
    weekly_pay
  ))

df_ok <- df_ok %>% mutate(
  pred_pay       = predict(model, newdata = .),
  weekly_pay_imp = if_else(is.na(weekly_pay), pred_pay, weekly_pay)
)

df_ok <- df_ok %>% select(-pred_pay) %>% arrange(ncdsid, age)
df_ok <- df_ok %>% mutate(
  weekly_pay_imp = if_else(weekly_pay_imp < 0, 0, weekly_pay_imp)
)


df_ok <- df_ok %>%
  group_by(ncdsid) %>%
  filter(n() == 3) %>%
  ungroup()


# LINEAR Interpolation
## 1.  Add helper columns ────────────────
df_ok <- df_ok %>% 
  mutate(
    month_idx         = round(age * 12L),         # age in *whole* months
    monthly_pay_imp   = weekly_pay_imp * 4.333     # 52 ÷ 12
  )

## 2.  Interpolate month-by-month wages ───
# helper that returns a tibble for one id
make_month_grid <- function(d){
  # keep only rows with a non-missing wage
  d <- d[!is.na(d$monthly_pay_imp), ]
  if(nrow(d) == 0) return(NULL)
  
  full_months <- seq(min(d$month_idx), max(d$month_idx))  # month grid
  
  # linear interpolation (rule = 2 = carry endpoints outside range if needed)
  interp <- approx(
    x   = d$month_idx,
    y   = d$monthly_pay_imp,
    xout= full_months,
    rule= 2L
  )$y
  
  tibble(
    ncdsid      = d$ncdsid[1],
    month_idx   = full_months,
    monthly_pay = interp
  )
}

df_monthly <- df_ok %>% 
  arrange(ncdsid, month_idx) %>% 
  group_by(ncdsid) %>% 
  group_modify(~make_month_grid(.x)) %>% 
  ungroup()

## 3.  Aggregate to lifetime earnings ─────
df_lifetime <- df_monthly %>% 
  group_by(ncdsid) %>% 
  summarise(
    lifetime_earn = sum(monthly_pay, na.rm = TRUE),  # nominal £
    .groups = "drop"
  )

## 4.  Inspect one id (optional) ───────────
# df_monthly %>% filter(ncdsid == "N11364S") %>% head()
# df_lifetime  %>% filter(ncdsid == "N11364S")

write.csv(df_lifetime, "/home/semipro321/OneDrive/School/McGill/Research Projects/Essay/Data/lifetime_earnings.csv", row.names = FALSE)
