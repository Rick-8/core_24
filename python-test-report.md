# Python Test Report

## Test Summary

Found 29 test(s).

- **Total Tests Run:** 29
- **Tests Passed:** 29
- **Duration:** 85.600 seconds

---

## Database Setup
- **Test Database:** test_mama_wimp_saint_886914

### Operations Performed:
- Synchronizing unmigrated apps: allauth, ckeditor, django_extensions, messages, staticfiles, widget_tweaks
- Applying migrations:
    - account, admin, auth, bookings, contenttypes, join_up, sessions, sites, socialaccount, staff_panel

---

## System Check Issues
1. **ckeditor**: 
   - django-ckeditor bundles CKEditor 4.22.1, which is no longer supported and has unfixed security issues. Consider switching to CKEditor 5 or an updated CKEditor 4 LTS.
   
2. **URLs**:
   - Warning: URL namespace 'staff_panel' isn't unique. You may not be able to reverse all URLs in this namespace.

---

## Tests Results

### Bookings App

- **test_delete_profile_success**: OK
- **test_booking_slot_full**: OK
- **test_cancel_booking**: OK
- **test_logout_redirects**: OK
- **test_home_page**: OK
- **test_logged_out_page**: OK

### Join Up App

- **test_delete_membership_invalid_method**: OK
- **test_delete_membership_success**: OK
- **test_edit_membership_post_valid_data**: OK
- **test_join_up_view_get**: OK
- **test_join_up_view_post_valid**: OK
- **test_create_membership_invalid_data**: OK
- **test_create_membership_not_logged_in**: OK
- **test_create_membership_success**: OK
- **test_membership_list_view**: OK

### Staff Panel App

- **test_create_user_access_for_staff**: OK
- **test_create_user_post_valid_data**: OK
- **test_delete_user_as_superuser**: OK
- **test_delete_user_without_login**: OK
- **test_get_reset_password_form**: OK
- **test_reset_password_as_superuser**: OK
- **test_staff_dashboard_access_denied_for_non_staff**: OK
- **test_staff_dashboard_access_granted_for_staff**: OK
- **test_staff_dashboard_redirects_anonymous_users**: OK
- **test_delete_join_request_success_for_staff**: OK
- **test_toggle_user_active_as_staff**: OK

---

## Conclusion

All tests passed successfully.



## Below is the original test data.


PS C:\Users\rick_\Documents\vscode-projects\gym_core_24\core_24> python manage.py test --verbosity=2
Found 29 test(s).
Creating test database for alias 'default' ('test_mama_wimp_saint_886914')...
Operations to perform:
  Synchronize unmigrated apps: allauth, ckeditor, django_extensions, messages, staticfiles, widget_tweaks
  Apply all migrations: account, admin, auth, bookings, contenttypes, join_up, sessions, sites, socialaccount, staff_panel
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying account.0001_initial... OK
  Applying account.0002_email_max_length... OK
  Applying account.0003_alter_emailaddress_create_unique_verified_email... OK
  Applying account.0004_alter_emailaddress_drop_unique_email... OK
  Applying account.0005_emailaddress_idx_upper_email... OK
  Applying account.0006_emailaddress_lower... OK
  Applying account.0007_emailaddress_idx_email... OK
  Applying account.0008_emailaddress_unique_primary_email_fixup... OK
  Applying account.0009_emailaddress_unique_primary_email... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying bookings.0001_initial... OK
  Applying bookings.0002_remove_booking_active_membership_and_more... OK
  Applying bookings.0003_alter_profile_membership_number... OK
  Applying bookings.0004_booking_closed_for_maintenance... OK
  Applying bookings.0005_closedday... OK
  Applying bookings.0006_remove_profile_id_alter_profile_user... OK
  Applying join_up.0001_initial... OK
  Applying join_up.0002_membership... OK
  Applying join_up.0003_alter_membership_description... OK
  Applying join_up.0004_customer_status... OK
  Applying join_up.0005_membership_active... OK
  Applying sessions.0001_initial... OK
  Applying sites.0001_initial... OK
  Applying sites.0002_alter_domain_unique... OK
  Applying socialaccount.0001_initial... OK
  Applying socialaccount.0002_token_max_lengths... OK
  Applying socialaccount.0003_extra_data_default_dict... OK
  Applying socialaccount.0004_app_provider_id_settings... OK
  Applying socialaccount.0005_socialtoken_nullable_app... OK
  Applying socialaccount.0006_alter_socialaccount_extra_data... OK
  Applying staff_panel.0001_initial... OK
System check identified some issues:

WARNINGS:
?: (ckeditor.W001) django-ckeditor bundles CKEditor 4.22.1 which isn't supported anymore and which does have unfixed security issues, see for example https://ckeditor.com/cke4/release/CKEditor-4.24.0-LTS . You should consider strongly switching to a different editor (maybe CKEditor 5 respectively django-ckeditor-5 after checking whether the CKEditor 5 license terms work for you) or switch to the non-free CKEditor 4 LTS package. See https://ckeditor.com/ckeditor-4-support/ for more on this. (Note! This notice has been added by the django-ckeditor developers and we are not affiliated with CKSource and were not involved in the licensing change, so please refrain from complaining to us. Thanks.)
?: (urls.W005) URL namespace 'staff_panel' isn't unique. You may not be able to reverse all URLs in this namespace

System check identified 2 issues (0 silenced).
test_delete_profile_success (bookings.tests.DeleteProfileTestCase.test_delete_profile_success) ... ok
test_booking_slot_full (bookings.tests.TestBookSlot.test_booking_slot_full)
Test that the booking fails when there are already 50 bookings ... ok
test_cancel_booking (bookings.tests.TestBookSlot.test_cancel_booking)
Test that a user can successfully cancel their booking. ... ok
test_logout_redirects (bookings.tests.TestCustomLogout.test_logout_redirects)
Test that the user is logged out and redirected ... Expected URL: /logged_out/, Actual Redirect: /logged_out/
ok
test_home_page (bookings.tests.TestHomePage.test_home_page)
Test that the home page renders correctly. ... ok
test_logged_out_page (bookings.tests.TestLoggedOut.test_logged_out_page)
Test that the 'logged_out' page renders correctly. ... ok
test_delete_membership_invalid_method (join_up.tests.DeleteMembershipTestCase.test_delete_membership_invalid_method)
Test invalid method (GET instead of POST). ... ok
test_delete_membership_success (join_up.tests.DeleteMembershipTestCase.test_delete_membership_success)
Test successful deletion of a membership. ... ok
test_edit_membership_post_valid_data (join_up.tests.EditMembershipViewTest.test_edit_membership_post_valid_data)
Test the POST request to edit a membership with valid data. ... ok
test_join_up_view_get (join_up.tests.JoinUpViewTest.test_join_up_view_get)
Test the GET request to the JoinUp view. ... ok
test_join_up_view_post_valid (join_up.tests.JoinUpViewTest.test_join_up_view_post_valid)
Test the POST request to the JoinUp view with valid data. ... ok
test_create_membership_invalid_data (join_up.tests.MembershipCreateViewTest.test_create_membership_invalid_data)
Test creation of a new membership with invalid data. ... ok
test_create_membership_not_logged_in (join_up.tests.MembershipCreateViewTest.test_create_membership_not_logged_in)
Test that an unauthenticated user is redirected to the login page. ... ok
test_create_membership_success (join_up.tests.MembershipCreateViewTest.test_create_membership_success)
Test successful membership creation. ... ok
Test the POST request to edit a membership with valid data. ... ok
test_join_up_view_get (join_up.tests.JoinUpViewTest.test_join_up_view_get)
Test the GET request to the JoinUp view. ... ok
test_join_up_view_post_valid (join_up.tests.JoinUpViewTest.test_join_up_view_post_valid)
Test the POST request to the JoinUp view with valid data. ... ok
test_create_membership_invalid_data (join_up.tests.MembershipCreateViewTest.test_create_membership_invalid_data)
Test creation of a new membership with invalid data. ... ok
test_create_membership_not_logged_in (join_up.tests.MembershipCreateViewTest.test_create_membership_not_logged_in)
Test that an unauthenticated user is redirected to the login page. ... ok
test_create_membership_success (join_up.tests.MembershipCreateViewTest.test_create_membership_success)
Test successful membership creation. ... ok
test_join_up_view_get (join_up.tests.JoinUpViewTest.test_join_up_view_get)
Test the GET request to the JoinUp view. ... ok
test_join_up_view_post_valid (join_up.tests.JoinUpViewTest.test_join_up_view_post_valid)
Test the POST request to the JoinUp view with valid data. ... ok
test_create_membership_invalid_data (join_up.tests.MembershipCreateViewTest.test_create_membership_invalid_data)
Test creation of a new membership with invalid data. ... ok
test_create_membership_not_logged_in (join_up.tests.MembershipCreateViewTest.test_create_membership_not_logged_in)
Test that an unauthenticated user is redirected to the login page. ... ok
test_create_membership_success (join_up.tests.MembershipCreateViewTest.test_create_membership_success)
Test successful membership creation. ... ok
Test the GET request to the JoinUp view. ... ok
test_join_up_view_post_valid (join_up.tests.JoinUpViewTest.test_join_up_view_post_valid)
Test the POST request to the JoinUp view with valid data. ... ok
test_create_membership_invalid_data (join_up.tests.MembershipCreateViewTest.test_create_membership_invalid_data)
Test creation of a new membership with invalid data. ... ok
test_create_membership_not_logged_in (join_up.tests.MembershipCreateViewTest.test_create_membership_not_logged_in)
Test that an unauthenticated user is redirected to the login page. ... ok
test_create_membership_success (join_up.tests.MembershipCreateViewTest.test_create_membership_success)
Test successful membership creation. ... ok
Test the POST request to the JoinUp view with valid data. ... ok
test_create_membership_invalid_data (join_up.tests.MembershipCreateViewTest.test_create_membership_invalid_data)
Test creation of a new membership with invalid data. ... ok
test_create_membership_not_logged_in (join_up.tests.MembershipCreateViewTest.test_create_membership_not_logged_in)
Test that an unauthenticated user is redirected to the login page. ... ok
test_create_membership_success (join_up.tests.MembershipCreateViewTest.test_create_membership_success)
Test successful membership creation. ... ok
test_create_membership_not_logged_in (join_up.tests.MembershipCreateViewTest.test_create_membership_not_logged_in)
Test that an unauthenticated user is redirected to the login page. ... ok
test_create_membership_success (join_up.tests.MembershipCreateViewTest.test_create_membership_success)
Test successful membership creation. ... ok
test_membership_list_view (join_up.tests.MembershipListViewTest.test_membership_list_view)
test_create_membership_success (join_up.tests.MembershipCreateViewTest.test_create_membership_success)
Test successful membership creation. ... ok
test_membership_list_view (join_up.tests.MembershipListViewTest.test_membership_list_view)
Test the GET request to view the list of memberships. ... ok
Test successful membership creation. ... ok
test_membership_list_view (join_up.tests.MembershipListViewTest.test_membership_list_view)
Test the GET request to view the list of memberships. ... ok
test_membership_list_view (join_up.tests.MembershipListViewTest.test_membership_list_view)
Test the GET request to view the list of memberships. ... ok
Test the GET request to view the list of memberships. ... ok
test_create_user_access_for_staff (staff_panel.tests.CreateUserTest.test_create_user_access_for_staff)
Ensure only staff users can access the create user page. ... ok
test_create_user_access_for_staff (staff_panel.tests.CreateUserTest.test_create_user_access_for_staff)
Ensure only staff users can access the create user page. ... ok
test_create_user_post_valid_data (staff_panel.tests.CreateUserTest.test_create_user_post_valid_data)
Ensure only staff users can access the create user page. ... ok
test_create_user_post_valid_data (staff_panel.tests.CreateUserTest.test_create_user_post_valid_data)
test_create_user_post_valid_data (staff_panel.tests.CreateUserTest.test_create_user_post_valid_data)
Ensure a staff user can create a user successfully. ... ok
Ensure a staff user can create a user successfully. ... ok
test_delete_user_as_superuser (staff_panel.tests.DeleteUserTest.test_delete_user_as_superuser)
test_delete_user_as_superuser (staff_panel.tests.DeleteUserTest.test_delete_user_as_superuser)
Test that a superuser can delete a user successfully. ... ok
Test that a superuser can delete a user successfully. ... ok
test_delete_user_without_login (staff_panel.tests.DeleteUserTest.test_delete_user_without_login)
Test that an unauthenticated user is redirected to the login page. ... ok
test_delete_user_without_login (staff_panel.tests.DeleteUserTest.test_delete_user_without_login)
Test that an unauthenticated user is redirected to the login page. ... ok
test_get_reset_password_form (staff_panel.tests.ResetPasswordTest.test_get_reset_password_form)
Test accessing the password reset form via GET request. ... ok
Test that an unauthenticated user is redirected to the login page. ... ok
test_get_reset_password_form (staff_panel.tests.ResetPasswordTest.test_get_reset_password_form)
Test accessing the password reset form via GET request. ... ok
test_reset_password_as_superuser (staff_panel.tests.ResetPasswordTest.test_reset_password_as_superuser)
Test resetting the password as a superuser. ... ok
test_get_reset_password_form (staff_panel.tests.ResetPasswordTest.test_get_reset_password_form)
Test accessing the password reset form via GET request. ... ok
test_reset_password_as_superuser (staff_panel.tests.ResetPasswordTest.test_reset_password_as_superuser)
Test resetting the password as a superuser. ... ok
Test accessing the password reset form via GET request. ... ok
test_reset_password_as_superuser (staff_panel.tests.ResetPasswordTest.test_reset_password_as_superuser)
Test resetting the password as a superuser. ... ok
test_staff_dashboard_access_denied_for_non_staff (staff_panel.tests.StaffDashboardJoinRequestTest.test_staff_dashboard_access_denied_for_non_staff)
test_reset_password_as_superuser (staff_panel.tests.ResetPasswordTest.test_reset_password_as_superuser)
Test resetting the password as a superuser. ... ok
test_staff_dashboard_access_denied_for_non_staff (staff_panel.tests.StaffDashboardJoinRequestTest.test_staff_dashboard_access_denied_for_non_staff)
Ensure non-staff users cannot access the staff dashboard. ... ok
test_staff_dashboard_access_denied_for_non_staff (staff_panel.tests.StaffDashboardJoinRequestTest.test_staff_dashboard_access_denied_for_non_staff)
Ensure non-staff users cannot access the staff dashboard. ... ok
test_staff_dashboard_access_granted_for_staff (staff_panel.tests.StaffDashboardJoinRequestTest.test_staff_dashboard_access_granted_for_staff)
Ensure staff users can access the staff dashboard. ... ok
Ensure non-staff users cannot access the staff dashboard. ... ok
test_staff_dashboard_access_granted_for_staff (staff_panel.tests.StaffDashboardJoinRequestTest.test_staff_dashboard_access_granted_for_staff)
Ensure staff users can access the staff dashboard. ... ok
test_staff_dashboard_access_granted_for_staff (staff_panel.tests.StaffDashboardJoinRequestTest.test_staff_dashboard_access_granted_for_staff)
Ensure staff users can access the staff dashboard. ... ok
Ensure staff users can access the staff dashboard. ... ok
test_staff_dashboard_redirects_anonymous_users (staff_panel.tests.StaffDashboardJoinRequestTest.test_staff_dashboard_redirects_anonymous_users)
Ensure unauthenticated users are redirected to the login page. ... ok
test_delete_join_request_success_for_staff (staff_panel.tests.StaffDashboardTest.test_delete_join_request_success_for_staff)
test_staff_dashboard_redirects_anonymous_users (staff_panel.tests.StaffDashboardJoinRequestTest.test_staff_dashboard_redirects_anonymous_users)
Ensure unauthenticated users are redirected to the login page. ... ok
test_delete_join_request_success_for_staff (staff_panel.tests.StaffDashboardTest.test_delete_join_request_success_for_staff)
Ensure staff can successfully delete a join request. ... ok
test_delete_join_request_success_for_staff (staff_panel.tests.StaffDashboardTest.test_delete_join_request_success_for_staff)
Ensure staff can successfully delete a join request. ... ok
test_staff_dashboard_access_denied_for_non_staff (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_access_denied_for_non_staff)
Ensure staff can successfully delete a join request. ... ok
test_staff_dashboard_access_denied_for_non_staff (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_access_denied_for_non_staff)
Ensure non-staff users cannot access the staff dashboard. ... ok
test_staff_dashboard_access_denied_for_non_staff (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_access_denied_for_non_staff)
Ensure non-staff users cannot access the staff dashboard. ... ok
test_staff_dashboard_access_granted_for_staff (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_access_granted_for_staff)
Ensure non-staff users cannot access the staff dashboard. ... ok
test_staff_dashboard_access_granted_for_staff (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_access_granted_for_staff)
Ensure staff users can access the staff dashboard. ... ok
test_staff_dashboard_access_granted_for_staff (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_access_granted_for_staff)
Ensure staff users can access the staff dashboard. ... ok
test_staff_dashboard_redirects_anonymous_users (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_redirects_anonymous_users)
Ensure staff users can access the staff dashboard. ... ok
test_staff_dashboard_redirects_anonymous_users (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_redirects_anonymous_users)
test_staff_dashboard_redirects_anonymous_users (staff_panel.tests.StaffDashboardTest.test_staff_dashboard_redirects_anonymous_users)
Ensure unauthenticated users are redirected to the login page. ... ok
Ensure unauthenticated users are redirected to the login page. ... ok
test_toggle_user_active_as_staff (staff_panel.tests.ToggleUserActiveTests.test_toggle_user_active_as_staff)
test_toggle_user_active_as_staff (staff_panel.tests.ToggleUserActiveTests.test_toggle_user_active_as_staff)
Test that a staff user can toggle a user's active status. ... ok
Test that a staff user can toggle a user's active status. ... ok


----------------------------------------------------------------------
Ran 29 tests in 85.600s

OK
Destroying test database for alias 'default' ('test_mama_wimp_saint_886914')...
PS C:\Users\rick_\Documents\vscode-projects\gym_core_24\core_24>