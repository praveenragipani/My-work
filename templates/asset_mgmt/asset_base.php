<?php

// Relative to the site root
$root="..";
$page_name="Featured Alteryx Content";

// Initialize php objects
include $root . "/assets/php/init.php";

// get user vars from session
$user=get_user();
$user_id=$user['user_id'];
$user_full=$user['user_full'];
$user_first=$user['user_first'];
$user_last=$user['user_last'];
$user_admin=$user['user_admin'];
$site = new siteInfo;

if($user_id=="guest"){
    header('Location: '.$root.'/?msg=user_login&dest=dashboards');
}

?>
<!DOCTYPE html>
<html>
<head>

  <!-- Standard Meta -->
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <meta name="description" content="Marketing Analytics">
  <meta name="author" content="Taylor Cox">

  <!-- Site Properties -->
  <title>Marketing Analytics | <?php echo $page_name; ?></title>
  <link rel="icon" type="image/png" href="<?php echo $root; ?>/assets/images/favicon.png">
  <link rel="stylesheet" type="text/css" href="<?php echo $root; ?>/semantic/dist/semantic.min.css">
  <link rel="stylesheet" type="text/css" href="<?php echo $root; ?>/assets/css/cfb.css">
  <link rel="icon" src="<?php echo $root; ?>/assets/images/student_logo.png">
</head>

<!-- Body -->
<body>

    <!-- Sidebar Menu -->
    <div class="ui sidebar inverted vertical labeled icon menu">
      <a href="<?php echo $root; ?>/" class="item">
        <img src="<?php echo $root; ?>/assets/images/student_logo.png" height="35" alt="CFBP">
      </a>
      <a href="<?php echo $root; ?>/" class="item">
        <i class="green home icon"></i>
        Home
      </a>

      <?php
          if($user_id=='guest'){
            echo "<a href='?msg=user_login&dest=apps' class='login-button item'>
                    <i class='laptop icon'></i>
                    Alteryx
                  </a>
                  <a href='?msg=user_login&dest=dashboards' class='login-button item'>
                    <i class='dashboard icon'></i>
                    Tableau
                  </a>
                  <a href='?msg=user_login&dest=team' class='login-button item'>
                    <i class='group icon'></i>
                    Our Team
                  </a>";
          }else{
              echo "<a href='$root/apps' class='item'>
                      <!-- <i class='laptop icon'></i> -->
                      <img class='ui centered mini image p-b-1' src='$root/assets/images/alteryx_icon.png'>
                      Alteryx
                    </a>
                    <a href='$root/dashboards' class='item'>
                      <!-- <i class='dashboard icon'></i> -->
                      <img class='ui centered mini image p-b-1' src='$root/assets/images/tableau-icon.png'>
                      Tableau
                    </a>
                    <a href='$root/team' class='item'>
                      <i class='yellow group icon'></i>
                      The Team
                    </a>";
                    if($user_admin=='yes'){
                      echo "<a href='$root/admin' class='item'>
                              <i class='red settings icon'></i>
                              Admin
                            </a>";
                    }
          }
      ?>
    </div>

    <!-- Body / Main Content -->
    <div class="pusher wrapper">

      <!-- Horizontal Menu -->

        <div class="ui inverted massive top fixed menu">
          <!-- <div class="item"> -->
          <a href="<?php echo $root; ?>/">
            <img src="<?php echo $root; ?>/assets/images/student_logo.png" class="image" height="32" style="margin: 10px 10px 0px 10px" alt="BCBSNC">
          </a>
          <!-- </div> -->
          <a class="view-ui item">
            <i class="sidebar icon"></i> Menu
          </a>
          <div class="ui inverted category search item public-search">
            <div class="ui transparent icon input">
              <input class='prompt' style='color:#ffffff;' type="text" placeholder="Search content...">
              <i class="inverted search link icon"></i>
            </div>
            <div class="results"></div>
          </div>
          <?php
            if($user_id=='guest'){
                echo "<a class='right menu item login-button'>
                        <i class='blue sign in icon'></i> Login
                      </a>";
            }else{
              $visitor = new siteUser($user_id);
              $vAvatar = $root.$visitor->avatar;
              echo "<span style='width: 100%;'>
                      <img style='margin: 0px 0px; padding: 0px 0px; float: right;' height='52' src='$vAvatar'>
                    </span>
                    <a class='right menu item'>
                      <div class='ui dropdown'>
                        <div class='text'>$user_full</div>
                        <i class='dropdown icon'></i>
                        <div class='menu'>
                          <div class='item sign-out'>
                            <i class='red sign out icon'></i>
                            Sign Out
                          </div>
                        </div>
                      </div>
                    </a>";
            }
          ?>
        </div>

<!-- Main Content -->
<div class="ui container p-t-5">
  <div class="ui segment">
    <span></span>
    <span class="ui huge header">
      <i class="dashboard icon"></i>
        <?php echo $page_name; ?>
    </span>
    &nbsp;&nbsp;&nbsp;
    <i class='green refresh icon'></i>
     <?php
      $sql="SELECT DATE_FORMAT(MAX(last_refreshed),'%c/%e/%Y at %l:%i %p') as refreshed FROM mtech.alteryx_apps";
        $con=db_connect();
        $res=mysqli_query($con,$sql);
        $arr=mysqli_fetch_array($res);
        $refr=$arr['refreshed'];

        echo "Updated $refr";
    ?>   
    <?php


    $type=$_GET["type"];
    $studio=$_GET["studio"];
    $product=$_GET["product"]; 
    $capability=$_GET["capability"];

    $source=$_GET["source"];
    $area=$_GET["area"];
    $owner=$_GET["owner"];
    $developer=$_GET["developer"];
    $sort=$_GET["sort"];

    $s_1 = "";
    $s_2 = "";
    $s_3 = "";
    $s_4 = "";

    if(!$sort || $sort==""){
      $sort_val='runcount';
      $sort_label='Popularity';
      $s_1 = "active ";
    }elseif($sort=="runcount"){
      $sort_val=$sort;
      $sort_label="Popularity";
      $s_1 = "active ";
    }elseif($sort=="name"){
      $sort_val=$sort;
      $sort_label="Content Name";
      $s_2 = "active ";
    }elseif($sort=="modified"){
      $sort_val=$sort;
      $sort_label="Last Modified";
      $s_3 = "active ";
    }elseif($sort=="created"){
      $sort_val=$sort;
      $sort_label="Published";
      $s_4 = "active ";
    }else{
      $sort_val='runcount';
      $sort_label='Popularity';
      $s_1 = "active ";
    }

   // data sources
    if(!$source || $source=="" || $source=="All"){
      $source_val='0';
      $source_label='All';
      $source_desc='All Data Sources';
    }else{
      $source_arr = getFilter('mtech.data_sources',$source);
      $source_val=$source_arr['id'];
      $source_label=$source_arr['label'];
      $source_desc=$source_arr['desc'];
    }

    // product group
    if(!$product || $product=="" || $product=="All"){
      $product_val='0';
      $product_label='All';
      $product_desc='All Product Groups';
    }else{
      $product_arr = getFilter('mtech.product_group',$product);
      $product_val=$product_arr['id'];
      $product_label=$product_arr['label'];
      $product_desc=$product_arr['desc'];
    }

    // capability
    if(!$capability || $capability=="" || $capability=="All"){
      $capability_val='0';
      $capability_label='All';
      $capability_desc='All Capabilities';
    }else{
      $capability_arr = getFilter('mtech.capability',$capability);
      $capability_val=$capability_arr['id'];
      $capability_label=$capability_arr['label'];
      $capability_desc=$capability_arr['desc'];
    }

    // business area
    if(!$area || $area=="" || $area=="All"){
      $area_val='0';
      $area_label='All';
      $area_desc='All Business Areas';
    }else{
      $area_arr = getFilter('mtech.bus_area',$area);
      $area_val=$area_arr['id'];
      $area_label=$area_arr['label'];
      $area_desc=$area_arr['desc'];
    }

    // business owner
    if(!$owner || $owner=="" || $owner=="All"){
      $owner_val='0';
      $owner_label='All';
      $owner_desc='All Business Owners';
    }else{
      $owner_val=$owner;
      $owner_arr = getADUser($owner);
      $owner_label = $owner_arr['display_name'];
      $owner_desc = $owner_label;
    }

    // developer
    if(!$developer || $developer=="" || $developer=="All"){
      $developer_val='0';
      $developer_label='All';
      $developer_desc='All Developers';
    }else{
      $developer_val=$developer;
      $developer_arr = getADUser($developer);
      $developer_label = $developer_arr['display_name'];
      $developer_desc = $developer_label;
    }

    if(!$type || $type=="" || $type=="App"){
      $type_val='App';
      $type_label='Application';
    }else{
      $type_val='Workflow';
      $type_label='Workflow';
    }

    if(!$studio || $studio==""){
      $studio_val='1';
      $studio_label='Marketing Analytics';
    } else {
      $studio_val=$studio;
    }

    $type_list = "<a href='?type=App&studio=$studio_val&product=$product_val&capability=$capability_val&area=$area_val&owner=$owner_val&developer=$developer_val&source=$source_val&sort=$sort_val' class='item'>Application</a>
      <a href='?type=Workflow&studio=$studio_val&product=$product_val&capability=$capability_val&area=$area_val&owner=$owner_val&developer=$developer_val&source=$source_val&sort=$sort_val' class='item'>Workflow</a>";

    $studioQry="SELECT
              s.id,
              s.studio_name
              FROM mtech.alteryx_studios s
              GROUP BY 1,2
              ORDER BY 2";

        $studioRes=mysqli_query($con,$studioQry);
        $studio_list="";
        while($studioArr=mysqli_fetch_array($studioRes)){
          $studio_name=$studioArr['studio_name'];
          $studio_id=$studioArr['id'];
          $studio_list.="<a href='?type=$type_val&studio=$studio_id&product=$product_val&capability=$capability_val&area=$area_val&owner=$owner_val&developer=$developer_val&source=$source_val&sort=$sort_val' class='item'>$studio_name</a>";
        }

      $curStudioQry="SELECT s.studio_name FROM mtech.alteryx_studios s WHERE s.id = '$studio_val' GROUP BY 1";
      $curStudioRes=mysqli_query($con,$curStudioQry);
      $curStudioArr=mysqli_fetch_array($curStudioRes);
      $studio_label=$curStudioArr['studio_name'];  

      // current URL
      // $_baseUrl = "?type=$type_val&studio=$studio_val&product=$product_val&capability=$capability_val&area=$area_val&owner=$owner_val&developer=$developer_val&source=$source_val&sort=$sort_val";

      $baseUrl = "?type=$type_val&studio=$studio_val&capability=$capability_val&area=$area_val&owner=$owner_val&developer=$developer_val&sort=$sort_val";
      $source_list = getFilterList('All','source','mtech.data_sources',$baseUrl);

      $baseUrl = "?type=$type_val&studio=$studio_val&capability=$capability_val&area=$area_val&owner=$owner_val&developer=$developer_val&source=$source_val&sort=$sort_val";
      $product_list = getFilterList('All','product','mtech.product_group',$baseUrl);

      $baseUrl = "?type=$type_val&studio=$studio_val&product=$product_val&area=$area_val&owner=$owner_val&developer=$developer_val&source=$source_val&sort=$sort_val";
      $capability_list = getFilterList('All','capability','mtech.capability',$baseUrl);

      $baseUrl = "?type=$type_val&studio=$studio_val&product=$product_val&capability=$capability_val&owner=$owner_val&developer=$developer_val&source=$source_val&sort=$sort_val";
      $area_list = getFilterList('All','area','mtech.bus_area',$baseUrl);

      $baseUrl = "?type=$type_val&studio=$studio_val&product=$product_val&capability=$capability_val&area=$area_val&developer=$developer_val&source=$source_val&sort=$sort_val";
      $owner_list = getOwnerListAYX('All','owner',$baseUrl,$type_val,$studio_val);

      $baseUrl = "?type=$type_val&studio=$studio_val&product=$product_val&capability=$capability_val&area=$area_val&owner=$owner_val&source=$source_val&sort=$sort_val";
      $developer_list = getDevListAYX('All','developer',$baseUrl,$type_val,$studio_val);

      $baseUrl = "?type=$type_val&studio=$studio_val&product=$product_val&capability=$capability_val&area=$area_val&owner=$owner_val&source=$source_val&developer=$developer_val";

      $sort_buttons =  "<div class='ui center aligned basic segment'>
                          <div class='ui compact buttons'>
                            <a href='" . $baseUrl . "&sort=runcount' class='ui compact ". $s_1 . "button' data-tooltip='Sort by Run Count' data-inverted=''>
                              <i class='sort numeric descending icon'></i>Popularity
                            </a>
                            <a href='" . $baseUrl . "&sort=name' class='ui compact ". $s_2 . "button' data-tooltip='Sort by Name' data-inverted=''>
                              <i class='sort alphabet ascending icon'></i>Name
                            </a>
                            <a href='" . $baseUrl . "&sort=modified' class='ui compact ". $s_3 . "button' data-tooltip='Sort by Date Modified' data-inverted=''>
                              <i class='sort content descending icon'></i>Modified
                            </a>
                            <a href='" . $baseUrl . "&sort=created' class='ui compact ". $s_4 . "button' data-tooltip='Sort by Date Published' data-inverted=''>
                              <i class='sort content descending icon'></i>Published
                            </a>
                          </div>
                        </div>";

  ?>
  <!-- FILTER BLOCK -->
  <div class="ui inverted segment">
    <div class="ui inverted form">

        <!-- first row filters -->
        <div class="four fields">

          <div class="field">
            <label style="color:#2ECCFA;">Content Type</label>
            <div class="ui selection dropdown">
              <i class="dropdown icon"></i>
              <div class="text"><?php echo $type_label; ?></div>
              <div class="menu">
                <?php echo $type_list; ?>
              </div>
            </div>
          </div>
          <div class="field">
            <label style="color:#2ECCFA;">Studio</label>
            <div class="ui selection dropdown">
              <i class="dropdown icon"></i>
              <div class="text"><?php echo $studio_label; ?></div>
              <div class="menu">
                <?php echo $studio_list; ?>
              </div>
            </div>
          </div>
          <div class="field">
            <label style="color:#2ECCFA">Developer</label>
            <div class="ui selection dropdown">
              <i class="dropdown icon"></i>
              <div class="text"><?php echo $developer_label; ?></div>
              <div class="menu">
                <?php echo $developer_list; ?>
              </div>
            </div>
          </div>
          <div class="field">
            <label>Data Source</label>
            <div class="ui selection dropdown">
              <i class="dropdown icon"></i>
              <div class="text"><?php echo $source_label; ?></div>
              <div class="menu">
                <?php echo $source_list; ?>
              </div>
            </div>
          </div>

        </div>

        <!-- Second row filters -->
        <div class="four fields">

          <div class="field">
            <label>Business Area</label>
            <div class="ui selection dropdown">
              <i class="dropdown icon"></i>
              <div class="text"><?php echo $area_label; ?></div>
              <div class="menu">
                <?php echo $area_list; ?>
              </div>
            </div>
          </div>
          <div class="field">
            <label>Business Owner</label>
            <div class="ui selection dropdown">
              <i class="dropdown icon"></i>
              <div class="text"><?php echo $owner_label; ?></div>
              <div class="menu">
                <?php echo $owner_list; ?>
              </div>
            </div>
          </div>
          <div class="field">
            <label>Product Group</label>
            <div class="ui selection dropdown">
              <i class="dropdown icon"></i>
              <div class="text"><?php echo $product_label; ?></div>
              <div class="menu">
                <?php echo $product_list; ?>
              </div>
            </div>
          </div>
          <div class="field">
            <label>Capability</label>
            <div class="ui selection dropdown">
              <i class="dropdown icon"></i>
              <div class="text"><?php echo $capability_label; ?></div>
              <div class="menu">
                <?php echo $capability_list; ?>
              </div>
            </div>
          </div>

        </div>      
        
    </div>

    <span class="m-r-1">
        <i class="blue filter icon"></i>
        <span style="color:#2ECCFA;">=&nbsp;&nbsp;Alteryx</span>
    </span>
    <span><i class="filter icon"></i>=&nbsp;&nbsp;user-defined tags &amp; meta</span>

    <a href="./" class="ui basic mini grey right floated button">Reset Filters</a>

  </div>
  <?php

  $qry="SELECT
        a.app_id,
        a.package_type,
        a.app_name,
        CASE WHEN COALESCE(a.app_description,'No Description')='' THEN 'No Description' ELSE COALESCE(a.app_description,'No Description') END AS app_description,
        a.studio,
        a.public,
        a.app_url,
        a.app_image_url,
        a.author_lan_id,
        COALESCE(t.full,a.author_full) as author_full,
        a.run_count,
        DATE_FORMAT(a.created,'%b %e, %Y, %l:%i %p') as created,
        DATE_FORMAT(a.updated,'%b %e, %Y, %l:%i %p') as updated,
        COALESCE(c.status,'new') as status,
        COALESCE(c.content_id,'na') as content_id,
        c.description,
        c.data_sources,
        c.bus_area,
        c.bus_owner,
        c.product_group,
        c.capability,
        COALESCE(ms.avatar, 'doughboy.png') as avatar,
        COALESCE(t.title,'Unknown Title') as owner_title,
        COALESCE(mk.lan_id,'None') as user_kudos,
        ak.kudos as author_kudos,
        COUNT(DISTINCT(k.lan_id)) AS kudos,
        COUNT(DISTINCT(x.comment_id)) AS comments
        FROM mtech.content c
        INNER JOIN mtech.alteryx_apps a
          ON a.app_id=c.link_id
        INNER JOIN mtech.alteryx_studios s 
          ON a.studio_id = s.studio_id
        LEFT JOIN mtech.member_settings ms
          ON a.author_lan_id=ms.lan_id
        LEFT JOIN mtech.team_members t
          ON a.author_lan_id=t.lan_id
        LEFT JOIN mtech.kudos k
          ON c.content_id=k.content_id
        LEFT JOIN mtech.kudos mk
          ON c.content_id=mk.content_id
          AND mk.lan_id='$user_id'
        LEFT JOIN mtech.author_kudos ak
          ON t.lan_id=ak.author
        LEFT JOIN mtech.comments x
          ON c.content_id=x.content_id
        WHERE c.status='active' ";

        $qry.="AND a.package_type='$type_val' AND s.id='$studio_val' ";

        // DEVELOPER FILTER
        if($developer_val=="0"){
          // all owners
        }else{
          $qry.="AND a.author_lan_id='$developer_val' ";
        }

        // BUSINESS AREA FILTER
        if($area_val=="0"){
          // all business areas
        }else{
          $qry.="AND c.bus_area LIKE '%$area_val%' ";
        }

        // BUSINESS OWNER FILTER
        if($owner_val=="0"){
          // all business owners
        }else{
          $qry.="AND c.bus_owner = '$owner_val' ";
        }

        // DATA SOURCE FILTER
        if($source_val=="0"){
          // all product groups
        }else{
          $qry.="AND c.data_sources LIKE '%$source_val%' ";
        }

        // PRODUCT GROUP FILTER
        if($product_val=="0"){
          // all product groups
        }else{
          $qry.="AND c.product_group LIKE '%$product_val%' ";
        }

        // CAPABILITY FILTER
        if($capability_val=="0"){
          // all capabilities
        }else{
          $qry.="AND c.capability LIKE '%$capability_val%' ";
        }

        $qry.="GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21 ";

        if($sort=="runcount"){
          $qry.="ORDER BY a.run_count DESC";
        }elseif($sort=="name"){
          $qry.="ORDER BY a.app_name ASC";
        }elseif($sort=="modified"){
          $qry.="ORDER BY a.updated DESC";
        }elseif($sort=="created"){
          $qry.="ORDER BY a.created DESC";
        }else{
          $qry.="ORDER BY a.run_count DESC";
        }

        $res=mysqli_query($con,$qry);

        $appCount=mysqli_num_rows($res);
        // echo $qry;
        echo "<h4 class='ui horizontal divider header'>$appCount " . $type_val . "s</h4>";
        echo $sort_buttons;

        echo "<div class='ui divided very relaxed items'>";

        while($arr=mysqli_fetch_array($res)){
          $app_id=$arr['app_id'];
          $package_type=$arr['package_type'];
          $app_name=$arr['app_name'];
          $owner_id=$arr['author_lan_id'];
          $owner=$arr['author_full'];
          $owner_title=$arr['owner_title'];
          $image=$root."/".$arr['app_image_url'];
          $url="http://".$arr['app_url'];
          $run_count=$arr['run_count'];
          $created=$arr['created'];
          $modified=$arr['updated'];
          $status=$arr['status'];
          $content_id=$arr['content_id'];
          $description=$arr['description'];
          $dataSources=$arr['data_sources'];
          $busAreas=$arr['bus_area'];
          $busOwner=$arr['bus_owner'];
          $prodGroups=$arr['product_group'];
          $capes=$arr['capability'];
          $kudos=$arr['kudos'];
          $comments=$arr['comments'];
          $user_kudos=$arr['user_kudos'];
          $author_kudos=$arr['author_kudos'];
          $dataLabels="";
          $areaLabels="";
          $prodLabels="";
          $capeLabels="";

          // data source labels
          if(!$dataSources || $dataSources == ""){
            $dataLabels.="n/a";
          }else{
            $dsIn=str_replace(",","','",$dataSources);
            $dSql="SELECT
                    id,
                    label,
                    description
                  FROM mtech.data_sources
                  WHERE id IN('$dsIn')
                  GROUP BY 1,2,3 ORDER BY 2";
            $dRes=mysqli_query($con,$dSql);
            while($dArr=mysqli_fetch_array($dRes)){
              $dataId=$dArr['id'];
              $dataLabel=$dArr['label'];
              $dataDesc=$dArr['description'];
              $dataLabels.="<a href='?source=$dataId' class='ui small circular label' data-tooltip='$dataDesc' data-position='top right' data-inverted=''>$dataLabel</a>";
            }
          }

          // bus area labels
          if(!$busAreas || $busAreas == ""){
            $areaLabels.="n/a";
          }else{
            $baIn=str_replace(",","','",$busAreas);
            $baSql="SELECT
                      id,
                      label,
                      description
                    FROM mtech.bus_area
                    WHERE id IN('$baIn')
                    GROUP BY 1,2,3 ORDER BY 2";
            $baRes=mysqli_query($con,$baSql);
            while($baArr=mysqli_fetch_array($baRes)){
              $areaId=$baArr['id'];
              $areaLabel=$baArr['label'];
              $baDesc=$baArr['description'];
              $areaLabels.="<a href='?area=$areaId' class='ui small circular label' data-tooltip='$baDesc' data-position='top right' data-inverted=''>$areaLabel</a>";
            }
          }

          // prod groups labels
          if(!$prodGroups || $prodGroups == ""){
            $prodLabels.="n/a";
          }else{
            $pgIn=str_replace(",","','",$prodGroups);
            $pgSql="SELECT
                    id,
                    label,
                    description
                  FROM mtech.product_group
                  WHERE id IN('$pgIn')
                  GROUP BY 1,2,3 ORDER BY 2";
            $pgRes=mysqli_query($con,$pgSql);
            while($pgArr=mysqli_fetch_array($pgRes)){
              $prodId=$pgArr['id'];
              $prodLabel=$pgArr['label'];
              $pgDesc=$pgArr['description'];
              $prodLabels.="<a href='?product=$prodId' class='ui small circular label' data-tooltip='$pgDesc' data-position='top right' data-inverted=''>$prodLabel</a>";
            }
          }

          // capability labels
          if(!$capes || $capes == ""){
            $capeLabels.="n/a";
          }else{
            $cIn=str_replace(",","','",$capes);
            $cSql="SELECT
                    id,
                    label,
                    description
                  FROM mtech.capability
                  WHERE id IN('$cIn')
                  GROUP BY 1,2,3 ORDER BY 2";
            $cRes=mysqli_query($con,$cSql);
            while($cArr=mysqli_fetch_array($cRes)){
              $capeId=$cArr['id'];
              $capeLabel=$cArr['label'];
              $cDesc=$cArr['description'];
              $capeLabels.="<a href='?capability=$capeId' class='ui small circular label' data-tooltip='$cDesc' data-position='top right' data-inverted=''>$capeLabel</a>";
            }
          }

          $more=$root."/apps/view?id=".$content_id;
          if($user_kudos=="None"){
            $kudosStat="<a href='$more&kudos=true' class='ui mini statistic p-t-2' data-tooltip='Give Kudos!' data-position='top right' data-inverted=''>
                          <div class='value'>
                            <i class='green thumbs outline up icon'></i> $kudos
                          </div>
                        </a>";
          }else{
            $kudosStat="<div class='ui mini statistic p-t-2' data-tooltip=\"You've already given Kudos\" data-position='top right' data-inverted=''>
                          <div class='value'>
                            <i class='green thumbs outline up icon'></i> $kudos
                          </div>
                        </div>";
          }
          if((int) $comments > 1 || (int) $comments < 1){
            $commentStat="<a href='$more#comment-feed' class='ui mini statistic p-t-2' data-tooltip='$comments comments' data-position='top right' data-inverted=''>
                          <div class='value'>
                            <i class='blue talk outline icon'></i> $comments
                          </div>
                        </a>";
          }else{
            $commentStat="<a href='$more#comment-feed' class='ui mini statistic p-t-2' data-tooltip='$comments comment' data-position='top right' data-inverted=''>
                          <div class='value'>
                            <i class='blue talk outline icon'></i> $comments
                          </div>
                        </a>";
          }

          $avatar=$root."/assets/images/users/".$arr['avatar'];

          echo"<div class='item'>
                  <div class='image'>
                    <img src='$image' class='ui medium image'>
                  </div>
                  <div class='content'>";

                  // Right floated stuff could go here
                  // echo "<div class='right floated blah'>
                  //       </div>";

              echo "<a href='$url' target='_blank' class='ui large violet header' data-tooltip='View in the Alteryx Gallery' data-inverted=''>$app_name</a>
                      <div class='meta'>
                        developed by <a href='?developer=$owner_id' class='ui tiny header'>$owner</a>
                        <img class='ui avatar image popper' src='$avatar' data-html='<div class=\"ui items\"><div class=\"item\">
                          <a class=\"ui tiny image\">
                            <img src=\"$avatar\">
                          </a>
                          <div class=\"middle aligned content\">
                            <div class=\"header\">$owner</div>
                            <div class=\"description\">$owner_title</div>";

                              if($author_kudos>0){
                                echo  "<div class=\"extra\">
                                        <a>
                                          <i class=\"thumbs up outline icon\"></i>
                                          $author_kudos Kudos Received
                                        </a>
                                       </div>";
                              }

                    echo "</div>
                        </div></div>' data-variation='very wide'>"; // closes img popper

                echo "</div>"; // closes meta div

                echo "<div class='description'>";

                  if(!$busOwner || $busOwner == ""){
                    // no need to render
                  }else{

                      $busOwner_arr = getADUser($busOwner);
                      $busOwner_name = $busOwner_arr['display_name'];
                      $busOwner_title = $busOwner_arr['title'];

                      echo "<div class='m-b-1'><strong>Business Owner:&nbsp;&nbsp;&nbsp;</strong><a href='?owner=$busOwner' class='ui tiny blue header'>$busOwner_name</a>, $busOwner_title</div>";

                  }

                  echo "<div class='m-b-9'><strong>Business Area:&nbsp;&nbsp;&nbsp;</strong>$areaLabels</div>
                        <div class='m-b-9'><strong>Product Group:&nbsp;&nbsp;&nbsp;</strong>$prodLabels</div>
                        <!-- <div class='m-b-9'><strong>Data Sources:&nbsp;&nbsp;&nbsp;</strong>$dataLabels</div> -->
                        <div class=''><strong>Capability:&nbsp;&nbsp;&nbsp;</strong>$capeLabels</div>
                      </div>
                      <div class='extra'>
                                <div class='ui mini statistic p-t-2' data-tooltip='Run $run_count times' data-position='top center' data-inverted=''>
                                  <div class='value'>
                                    <i class='red lightning icon'></i> $run_count
                                  </div>
                                </div>
                                $kudosStat
                                $commentStat
                                <a href='$more' class='ui mini right floated basic blue button'>
                                  More...
                                </a>
                      </div>
                  </div>
                </div>";
        }
        echo "</div>";
        db_disconnect();
  ?>

  </div>
</div>
</div><!-- END PUSHER -->
<!-- Footer -->
<div class="ui inverted vertical footer segment">
  <div class="ui container">
    <div class="ui stackable inverted divided equal height stackable grid">
      <div class="three wide column">
        <h4 class="ui inverted header">About</h4>
        <div class="ui inverted link list">
          <a href="<?php echo $root; ?>/about" class="item">What we do..</a>
          <a href="mailto:<?php echo $site->contact; ?>" target="_top" class="item">Contact</a>
        </div>
      </div>
      <div class="three wide column">
        <h4 class="ui inverted header">Services</h4>
        <div class="ui inverted link list">
          <a href="<?php echo $root; ?>/member/account" class="item">Submit a Request</a>
          <a href="<?php echo $root; ?>/faq" class="item">FAQ</a>
        </div>
      </div>
      <div class="seven wide column">
        <img src="<?php echo $root; ?>/assets/images/student_logo.png" height="80" alt="CFBP">
      </div>
    </div>
  </div>
</div>
</body>

<div class="ui page dimmer">
  <div class="content">
    <div class="ui middle aligned center aligned stackable grid">
      <div class="computer only row">
        <div class="four wide column">
                    <h2 class="ui blue image header">
                      <img src="<?php echo $root; ?>/assets/images/student_logo.png" class="image">
                      <div class="content">
                        Login
                      </div>
                    </h2>
                    <form class="ui form"  action="<?php echo $root; ?>/assets/php/test_pass.php" method="post">
                      <div class="ui stacked segment">
                        <div class="field">
                          <div class="ui left icon input">
                            <i class="user icon"></i>
                            <input type="text" id="username" name="username" placeholder="LAN ID (U Number)">
                          </div>
                        </div>
                        <div class="field">
                          <div class="ui left icon input">
                            <i class="lock icon"></i>
                            <input type="password" name="password" placeholder="Password">
                          </div>
                        </div>
                        <input class="ui fluid blue submit button" type="submit" value="Login">
                        <div class="ui horizontal divider">
                        Or
                        </div>
                        <a class="login-cancel">Cancel</a>
                      </div>
                      <div class="ui error message"></div>

                    </form>
          </div>
        </div>
        <div class="tablet only row">
          <div class="eight wide column">
                      <h2 class="ui blue image header">
                        <img src="<?php echo $root; ?>/assets/images/student_logo.png" height="35" class="image">
                        <div class="content">
                          Login
                        </div>
                      </h2>
                      <form class="ui form"  action="<?php echo $root; ?>/assets/php/test_pass.php" method="post">
                        <div class="ui stacked segment">
                          <div class="field">
                            <div class="ui left icon input">
                              <i class="user icon"></i>
                              <input type="text" id="username" name="username" placeholder="LAN ID (U Number)">
                            </div>
                          </div>
                          <div class="field">
                            <div class="ui left icon input">
                              <i class="lock icon"></i>
                              <input type="password" name="password" placeholder="Password">
                            </div>
                          </div>
                          <input class="ui fluid blue submit button" type="submit" value="Login">
                          <div class="ui horizontal divider">
                          Or
                          </div>
                          <a class="login-cancel">Cancel</a>
                        </div>

                        <div class="ui error message"></div>

                      </form>
            </div>
        </div>
          <div class="mobile only row">
            <div class="column">
                        <h2 class="ui blue image header">
                          <img src="<?php echo $root; ?>/assets/images/student_logo.png" height="35" class="image">
                          <div class="content">
                            Login
                          </div>
                        </h2>
                        <form class="ui form"  action="<?php echo $root; ?>/assets/php/test_pass.php" method="post">
                          <div class="ui stacked segment">
                            <div class="field">
                              <div class="ui left icon input">
                                <i class="user icon"></i>
                                <input type="text" id="username" name="username" placeholder="LAN ID (U Number)">
                              </div>
                            </div>
                            <div class="field">
                              <div class="ui left icon input">
                                <i class="lock icon"></i>
                                <input type="password" name="password" placeholder="Password">
                              </div>
                            </div>
                            <input class="ui fluid blue submit button" type="submit" value="Login">
                            <div class="ui horizontal divider">
                            Or
                            </div>
                            <a class="login-cancel">Cancel</a>
                          </div>

                          <div class="ui error message"></div>

                        </form>
              </div>
          </div>
    </div>
  </div>
</div>

<!-- Javascript Load @ end of document to prevent bottlenecking page load -->
<script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
<script src="<?php echo $root; ?>/semantic/dist/semantic.min.js"></script>
<script src="<?php echo $root; ?>/assets/js/app.js"></script>
<script>

  var msg = "<?php echo $_GET['msg']; ?>";
  var user = "<?php echo $user_id; ?>";
  var dest = "<?php echo $_GET['dest']; ?>";

  if(msg=='user_login' && user=='guest'){
    $('.ui.page.dimmer').dimmer('show');
    $("#username").focus();
  }

  if(dest!=='' && dest!==undefined && dest!==null && user!=='guest'){
    url = "http://alteryx.bcbsnc.com/mtech/" + dest;
    window.location = url;
  }

  function refreshGviz(){

      $('#refresh_dimmer').dimmer('show');

      var str = "getWorkbooks.php?s=gviz";
      var xmlhttp = new XMLHttpRequest();
      var books;
      xmlhttp.onreadystatechange = function() {
          if (xmlhttp.readyState == XMLHttpRequest.DONE) {
            //  $('#refresh_dimmer').dimmer('hide');
            var response = $.parseJSON(xmlhttp.responseText);
            var wbCount = response["count"];
            books = response["books"];
            $("#dimmerHeader").html("Found " + wbCount + " workbooks on the GVIZ server...");
            var progBox = "<div class='ui indicating progress' data-value='1' data-total='" + wbCount + "' id='dimmerProgress'><div class='bar'><div class='progress'></div></div></div><span class='white text' id='dimmerMessage'>Loading GVIZ Workbooks</span>";
            $("#dimmerProgBox").html(progBox);


            var index;
            var matchedIndex=0;
            // for (index = 0; index < books.length; ++index) {
            for (index = 0; index < books.length; ++index) {
              var book=books[index];
              var str = "refreshWorkbook.php?s=gviz&id=" + book;
              $("#dimmerMessage").html(str);

              matchedIndex=index+1;

              if(matchedIndex < books.length){
                var last="no";
              }else{
                var last="yes";
              }
              // Fire off the request to /form.php
                  request = $.ajax({
                      url: "refreshWorkbook.php",
                      type: "post",
                      data: {s: 'gviz', id: book, eor: last}
                  });

                  // Callback handler that will be called on success
                  request.done(function (response, textStatus, jqXHR){
                      // Log a message to the console
                      $('#dimmerProgress')
                        .progress('increment')
                      ;
                      if(response=='finished'){
                        $('#refresh_dimmer').dimmer('hide');
                        $("#dimmerMessage").html("");
                        $("#dimmerProgBox").html("");
                        $("#dimmerHeader").html("");
                        location.reload();
                      }else{
                        $("#dimmerMessage").html(response);
                      }
                  });

            }
          }
      }
      xmlhttp.open("GET",str,true);
      xmlhttp.send();

  }

  function refreshVizdev(){

      $('#refresh_dimmer').dimmer('show');

      var str = "getWorkbooks.php?s=vizdev";
      var xmlhttp = new XMLHttpRequest();
      var books;
      xmlhttp.onreadystatechange = function() {
          if (xmlhttp.readyState == XMLHttpRequest.DONE) {
            //  $('#refresh_dimmer').dimmer('hide');
            var response = $.parseJSON(xmlhttp.responseText);
            var wbCount = response["count"];
            books = response["books"];
            $("#dimmerHeader").html("Found " + wbCount + " workbooks on the VIZDEV server...");
            var progBox = "<div class='ui indicating progress' data-value='1' data-total='" + wbCount + "' id='dimmerProgress'><div class='bar'><div class='progress'></div></div></div><span class='white text' id='dimmerMessage'>Loading VIZDEV Workbooks</span>";
            $("#dimmerProgBox").html(progBox);


            var index;
            var matchedIndex=0;
            // for (index = 0; index < books.length; ++index) {
            for (index = 0; index < books.length; ++index) {
              var book=books[index];
              var str = "refreshWorkbook.php?s=vizdev&id=" + book;
              $("#dimmerMessage").html(str);

              matchedIndex=index+1;

              if(matchedIndex < books.length){
                var last="no";
              }else{
                var last="yes";
              }
              // Fire off the request to /form.php
                  request = $.ajax({
                      url: "refreshWorkbook.php",
                      type: "post",
                      data: {s: 'vizdev', id: book, eor: last}
                  });

                  // Callback handler that will be called on success
                  request.done(function (response, textStatus, jqXHR){
                      // Log a message to the console
                      $('#dimmerProgress')
                        .progress('increment')
                      ;
                      if(response=='finished'){
                        $('#refresh_dimmer').dimmer('hide');
                        $("#dimmerMessage").html("");
                        $("#dimmerProgBox").html("");
                        $("#dimmerHeader").html("");
                        location.reload();
                      }else{
                        $("#dimmerMessage").html(response);
                      }
                  });

            }
          }
      }
      xmlhttp.open("GET",str,true);
      xmlhttp.send();

  }

</script>
</html>
