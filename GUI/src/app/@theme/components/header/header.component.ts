import {Component, ChangeDetectorRef} from '@angular/core';
import {GUIGlobal} from '../../../providers/GUIGlobal';
import {NbThemeService} from "@nebular/theme";

@Component({
  selector: 'ngx-header',
  styleUrls: ['./header.component.scss'],
  templateUrl: './header.component.html',
})
export class HeaderComponent {

  isMaximized: boolean = false;
  platform: string = (<any>window).apiPlatform;
  isDark = false;

  constructor(private cd: ChangeDetectorRef,
              public global: GUIGlobal,
              private themeService: NbThemeService) { }

  ngOnInit() {

    if (this.global.getGlobalVar('electronAvailable')) {
      this.initTheme();

      this.global.isWindowMaximized().then(res => {
        this.isMaximized = res;

        this.cd.markForCheck();
        this.cd.detectChanges();
      }).catch((err) => {
        console.log(err);
      });

      this.global.globalEmitter.subscribe(eventObj => {

        if (eventObj.name == "window_maximized") {
          //console.log("maximized event");
          this.isMaximized = true;

          this.cd.markForCheck();
          this.cd.detectChanges();
        }
        else if (eventObj.name == "window_unmaximized") {
          //console.log("unmaximized event");
          this.isMaximized = false;

          this.cd.markForCheck();
          this.cd.detectChanges();
        }
      });
    }
  }

  minimize() {
    this.global.minimizeWindow();
  }

  maximize() {
    this.global.maximizeWindow();
  }

  switchTheme() {
    if (this.isDark) {
      this.themeService.changeTheme('ootr-default');
      this.isDark = false;
      this.global.generator_settingsMap["theme"] = 'ootr-default';
    } else {
      this.themeService.changeTheme('ootr-dark');
      this.isDark = true;
      this.global.generator_settingsMap["theme"] = 'ootr-dark';
    }
    this.global.saveCurrentSettingsToFile();
  }

  close() {
    this.global.closeWindow();
  }

  private initTheme() {
    if (this.global.generator_settingsMap && this.global.generator_settingsMap["theme"]) {
      this.themeService.changeTheme(this.global.generator_settingsMap["theme"]);
      this.isDark = 'ootr-dark' === this.global.generator_settingsMap["theme"];
    }
  }
}
